from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
import secrets

from ..database import get_db
from ..models import Farmer, SoilTest, Location, WeatherRecord, Recommendation, Report
from ..schemas import *
from ..services.soil import analyze
from ..services.weather import fetch_weather
from ..ml.predict import predict
from ..rag.pipeline import retrieve
from ..agents.recommend import explain, compatibility
from ..services.report import build_report, build_bilingual_report

router = APIRouter(prefix="/api")


@router.get("/health")
def health(db: Session = Depends(get_db)):
    db.query(Farmer).count()
    return {"status": "ok", "database": "connected"}


@router.get("/system/status")
def system_status(db: Session = Depends(get_db)):
    return {
        "api": "online",
        "gateway": "disconnected",
        "farmer_configured": db.query(Farmer).count() > 0,
        "test_count": db.query(SoilTest).count()
    }


@router.post("/farmers", response_model=FarmerOut)
def create_farmer(payload: FarmerCreate, db: Session = Depends(get_db)):
    farmer = Farmer(**payload.model_dump())
    db.add(farmer)
    db.commit()
    db.refresh(farmer)
    return farmer


@router.get("/farmers/{farmer_id}", response_model=FarmerOut)
def get_farmer(farmer_id: int, db: Session = Depends(get_db)):
    farmer = db.get(Farmer, farmer_id)
    if not farmer:
        raise HTTPException(404, "Farmer not found")
    return farmer


def make_test_id(db):
    while True:
        value = f"KAI-{datetime.utcnow().year}-{secrets.randbelow(90000) + 10000}"
        if not db.query(SoilTest).filter_by(test_id=value).first():
            return value


def save_soil(payload, source, db):
    if not db.get(Farmer, payload.farmer_id):
        raise HTTPException(404, "Farmer not found")

    test = SoilTest(
        test_id=make_test_id(db),
        input_source=source,
        **payload.model_dump()
    )
    db.add(test)
    db.commit()
    db.refresh(test)
    return test


@router.post("/soil/manual", response_model=SoilTestOut)
def manual_soil(payload: SoilInput, db: Session = Depends(get_db)):
    return save_soil(payload, "Manual Input", db)


@router.post("/soil/read", response_model=SoilTestOut)
def sensor_soil(payload: SensorReading, db: Session = Depends(get_db)):
    data = SoilInput(
        farmer_id=payload.farmer_id,
        **payload.model_dump(exclude={"device_id", "timestamp"})
    )
    return save_soil(data, "Live IoT Sensor", db)


@router.get("/soil/latest")
def latest_soil(farmer_id: int | None = None, db: Session = Depends(get_db)):
    q = db.query(SoilTest).order_by(desc(SoilTest.created_at))
    if farmer_id:
        q = q.filter(SoilTest.farmer_id == farmer_id)
    test = q.first()
    return test if test else None


@router.post("/soil/analyze", response_model=SoilAnalysisOut)
def soil_analyze(test_id: str, db: Session = Depends(get_db)):
    test = db.query(SoilTest).filter_by(test_id=test_id).first()
    if not test:
        raise HTTPException(404, "Soil test not found")
    return analyze(test)


@router.post("/location/analyze")
def location_analyze(payload: LocationInput, db: Session = Depends(get_db)):
    farmer = db.get(Farmer, payload.farmer_id)
    if not farmer:
        raise HTTPException(404, "Farmer not found")

    loc = Location(
        farmer_id=farmer.id,
        village=farmer.village,
        taluka=farmer.taluka,
        district=farmer.district,
        state=farmer.state,
        latitude=payload.latitude,
        longitude=payload.longitude,
        source=(
            "GPS"
            if payload.latitude is not None and payload.longitude is not None
            else "farmer-entered"
        )
    )
    db.add(loc)
    db.commit()
    db.refresh(loc)

    return {
        "id": loc.id,
        "source": loc.source,
        "location": {
            "village": loc.village,
            "taluka": loc.taluka,
            "district": loc.district,
            "state": loc.state,
            "latitude": loc.latitude,
            "longitude": loc.longitude
        }
    }


@router.post("/weather/fetch")
async def weather_fetch(payload: WeatherRequest, db: Session = Depends(get_db)):
    farmer = db.get(Farmer, payload.farmer_id)
    if not farmer:
        raise HTTPException(404, "Farmer not found")

    data, error = await fetch_weather(payload.latitude, payload.longitude)
    if error:
        return {"available": False, "message": error}

    loc = Location(
        farmer_id=farmer.id,
        village=farmer.village,
        taluka=farmer.taluka,
        district=farmer.district,
        state=farmer.state,
        latitude=payload.latitude,
        longitude=payload.longitude,
        source="GPS"
    )
    db.add(loc)
    db.commit()
    db.refresh(loc)

    wr = WeatherRecord(location_id=loc.id, **data)
    db.add(wr)
    db.commit()

    return {"available": True, "weather": data}


@router.post("/crop/recommend", response_model=RecommendationResponse)
def recommend(test_id: str, db: Session = Depends(get_db)):
    test = db.query(SoilTest).filter_by(test_id=test_id).first()
    if not test:
        raise HTTPException(404, "Soil test not found")

    farmer = db.get(Farmer, test.farmer_id)
    analysis = analyze(test)

    ranked = predict({
        "nitrogen": test.nitrogen,
        "phosphorus": test.phosphorus,
        "potassium": test.potassium,
        "soil_moisture": test.soil_moisture,
        "air_temperature": test.air_temperature,
        "humidity": test.humidity
    })

    crops = [x["crop"] for x in ranked]
    rag_docs = retrieve(
        crops,
        f"{' '.join(crops)} {farmer.district} {farmer.state}"
    )

    db.query(Recommendation).filter_by(soil_test_id=test.id).delete()
    results = []

    for item in ranked:
        suit, soil, pref = compatibility(
            farmer.preferred_crop,
            item["crop"],
            analysis
        )

        exp = explain(
            item["crop"],
            analysis,
            farmer.preferred_crop,
            rag_docs
        )

        rec = Recommendation(
            soil_test_id=test.id,
            crop=item["crop"],
            ml_probability=item["ml_probability"],
            suitability=suit,
            soil_compatibility=soil,
            location_compatibility="Location entered by farmer",
            preference_compatibility=pref,
            explanation=exp
        )
        db.add(rec)
        results.append(rec)

    db.commit()

    note = None
    if farmer.preferred_crop:
        note = (
            "The preferred crop is shown as a separate farmer preference "
            "and does not override the model."
        )

    return {
        "test_id": test.test_id,
        "recommendations": results,
        "preferred_crop": farmer.preferred_crop,
        "preferred_crop_note": note
    }


@router.post("/soil-tests/{test_id}/report")
def create_report(test_id: str, db: Session = Depends(get_db)):
    test = db.query(SoilTest).filter_by(test_id=test_id).first()
    if not test:
        raise HTTPException(404, "Soil test not found")

    farmer = db.get(Farmer, test.farmer_id)
    analysis = analyze(test)

    recs = db.query(Recommendation).filter_by(soil_test_id=test.id).all()
    if not recs:
        raise HTTPException(
            400,
            "Generate crop recommendations before creating a report"
        )

    path = build_report(farmer, test, analysis, recs)

    existing = db.query(Report).filter_by(soil_test_id=test.id).first()
    if existing:
        existing.report_path = str(path)
    else:
        db.add(Report(soil_test_id=test.id, report_path=str(path)))

    db.commit()

    return {
        "test_id": test_id,
        "download_url": f"/api/reports/{test_id}"
    }


# English PDF download
@router.get("/reports/{test_id}")
def get_report(test_id: str, db: Session = Depends(get_db)):
    report = (
        db.query(Report)
        .join(SoilTest, Report.soil_test_id == SoilTest.id)
        .filter(SoilTest.test_id == test_id)
        .first()
    )

    if not report:
        raise HTTPException(404, "Report not found")

    return FileResponse(
        report.report_path,
        media_type="application/pdf",
        filename=f"{test_id}.pdf"
    )


# Bilingual English + Marathi PDF download
@router.get("/reports/{test_id}/bilingual")
def get_bilingual_report(test_id: str, db: Session = Depends(get_db)):
    test = db.query(SoilTest).filter_by(test_id=test_id).first()
    if not test:
        raise HTTPException(404, "Soil test not found")

    farmer = db.get(Farmer, test.farmer_id)
    analysis = analyze(test)

    recs = db.query(Recommendation).filter_by(soil_test_id=test.id).all()
    if not recs:
        raise HTTPException(
            400,
            "Generate crop recommendations before downloading the report"
        )

    path = build_bilingual_report(
        farmer,
        test,
        analysis,
        recs
    )

    return FileResponse(
        str(path),
        media_type="application/pdf",
        filename=f"{test_id}_bilingual.pdf"
    )


@router.get("/soil-tests", response_model=list[SoilTestOut])
def history(db: Session = Depends(get_db)):
    return db.query(SoilTest).order_by(desc(SoilTest.created_at)).all()


@router.get("/soil-tests/{test_id}", response_model=SoilTestOut)
def get_test(test_id: str, db: Session = Depends(get_db)):
    test = db.query(SoilTest).filter_by(test_id=test_id).first()
    if not test:
        raise HTTPException(404, "Soil test not found")
    return test


@router.post("/dev/simulate-soil-reading", response_model=SoilTestOut)
def simulate(payload: dict, db: Session = Depends(get_db)):
    farmer_id = int(payload.get("farmer_id", 0))
    if not farmer_id:
        raise HTTPException(400, "farmer_id is required")

    # Clearly developer-only simulated values.
    data = SoilInput(
        farmer_id=farmer_id,
        nitrogen=float(payload.get("nitrogen", 55)),
        phosphorus=float(payload.get("phosphorus", 35)),
        potassium=float(payload.get("potassium", 45)),
        soil_moisture=float(payload.get("soil_moisture", 50)),
        air_temperature=float(payload.get("air_temperature", 24)),
        humidity=float(payload.get("humidity", 68))
    )

    return save_soil(data, "Developer Simulator", db)