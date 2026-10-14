from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from datetime import datetime
from ..database import Base

class Farmer(Base):
    __tablename__ = "farmers"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    mobile = Column(String(20), nullable=False)
    village = Column(String(120), nullable=False)
    taluka = Column(String(120), nullable=False)
    district = Column(String(120), nullable=False)
    state = Column(String(120), nullable=False)
    farm_name = Column(String(120), nullable=True)
    preferred_crop = Column(String(80), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SoilTest(Base):
    __tablename__ = "soil_tests"
    id = Column(Integer, primary_key=True)
    test_id = Column(String(40), unique=True, nullable=False, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    input_source = Column(String(30), nullable=False)
    nitrogen = Column(Float, nullable=False)
    phosphorus = Column(Float, nullable=False)
    potassium = Column(Float, nullable=False)
    soil_moisture = Column(Float, nullable=False)
    air_temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(30), default="completed")

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    village = Column(String(120), nullable=False)
    taluka = Column(String(120), nullable=False)
    district = Column(String(120), nullable=False)
    state = Column(String(120), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    source = Column(String(40), default="farmer-entered")
    created_at = Column(DateTime, default=datetime.utcnow)

class WeatherRecord(Base):
    __tablename__ = "weather_records"
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    rainfall = Column(Float, nullable=True)
    weather_condition = Column(String(120), nullable=True)
    wind_speed = Column(Float, nullable=True)
    source = Column(String(80), nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow)

class Recommendation(Base):
    __tablename__ = "recommendations"
    id = Column(Integer, primary_key=True)
    soil_test_id = Column(Integer, ForeignKey("soil_tests.id"), nullable=False)
    crop = Column(String(80), nullable=False)
    ml_probability = Column(Float, nullable=True)
    suitability = Column(String(120), nullable=True)
    soil_compatibility = Column(String(120), nullable=True)
    location_compatibility = Column(String(120), nullable=True)
    weather_compatibility = Column(String(120), nullable=True)
    preference_compatibility = Column(String(120), nullable=True)
    explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True)
    soil_test_id = Column(Integer, ForeignKey("soil_tests.id"), nullable=False)
    report_path = Column(String(300), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
