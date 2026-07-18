from typing import Optional

from pydantic import BaseModel


class WeatherResponse(BaseModel):
    temperature: Optional[float] = None
    humidity: Optional[float] = None


class FireResponse(BaseModel):
    nearby_hotspots: int = 0
    risk: str = "Unknown"
    source: str = ""


class VegetationResponse(BaseModel):
    ndvi: Optional[float] = None
    health: str = "Unknown"


class AnalysisResponse(BaseModel):
    latitude: float
    longitude: float

    weather: WeatherResponse
    fire: FireResponse
    vegetation: VegetationResponse

    ecosystem_health: int
    risk: str

    recommendations: list[str]
