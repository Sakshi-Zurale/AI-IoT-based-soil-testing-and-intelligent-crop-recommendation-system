from pathlib import Path
import joblib
import pandas as pd

MODEL_PATH = Path(__file__).resolve().parent / "models" / "crop_model.joblib"

def ensure_model():
    if not MODEL_PATH.exists():
        from .train import train
        train()

def predict(data):
    ensure_model()
    bundle = joblib.load(MODEL_PATH)
    model = bundle["model"]
    row = pd.DataFrame([{
        "N": data["nitrogen"],
        "P": data["phosphorus"],
        "K": data["potassium"],
        "temperature": data["air_temperature"],
        "humidity": data["humidity"],
        "moisture": data["soil_moisture"],
    }])
    probs = model.predict_proba(row)[0]
    classes = list(model.classes_)
    ranked = sorted(
        [{"crop": classes[i], "ml_probability": float(probs[i])} for i in range(len(classes))],
        key=lambda x: x["ml_probability"], reverse=True
    )
    return ranked[:5]
