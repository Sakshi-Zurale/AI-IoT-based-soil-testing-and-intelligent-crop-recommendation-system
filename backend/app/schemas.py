from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class FarmerCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    mobile: str = Field(min_length=10, max_length=20)
    village: str = Field(min_length=2, max_length=120)
    taluka: str = Field(min_length=2, max_length=120)
    district: str = Field(min_length=2, max_length=120)
    state: str = Field(min_length=2, max_length=120)
    farm_name: Optional[str] = None
    preferred_crop: Optional[str] = None

class FarmerOut(FarmerCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class SoilInput(BaseModel):
    farmer_id: int
    nitrogen: float = Field(ge=0)
    phosphorus: float = Field(ge=0)
    potassium: float = Field(ge=0)
    soil_moisture: float = Field(ge=0, le=100)
    air_temperature: float
    humidity: float = Field(ge=0, le=100)

class SensorReading(SoilInput):
    device_id: str = Field(min_length=1, max_length=80)
    timestamp: Optional[datetime] = None

class SoilTestOut(BaseModel):
    id: int
    test_id: str
    farmer_id: int
    input_source: str
    nitrogen: float
    phosphorus: float
    potassium: float
    soil_moisture: float
    air_temperature: float
    humidity: float
    created_at: datetime
    status: str
    model_config = ConfigDict(from_attributes=True)

class RecommendationOut(BaseModel):
    crop: str
    ml_probability: Optional[float]
    suitability: str
    soil_compatibility: str
    location_compatibility: str
    weather_compatibility: str | None = None
    preference_compatibility: str
    explanation: str

class LocationInput(BaseModel):
    farmer_id: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class WeatherRequest(BaseModel):
    farmer_id: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class AnalysisParameter(BaseModel):
    value: float
    status: str
    interpretation: str

class SoilAnalysisOut(BaseModel):
    test_id: str
    parameters: dict

class RecommendationResponse(BaseModel):
    test_id: str
    recommendations: List[RecommendationOut]
    preferred_crop: Optional[str] = None
    preferred_crop_note: Optional[str] = None
