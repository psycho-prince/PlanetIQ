from pydantic import BaseModel

class AnalysisResponse(BaseModel):
    latitude: float
    longitude: float
    weather: dict
    ecosystem_health: int
    risk: str
