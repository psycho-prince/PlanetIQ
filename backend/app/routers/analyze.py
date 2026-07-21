from fastapi import APIRouter
from pydantic import BaseModel
from backend.app.services.weather_service import get_weather
from backend.app.services.health_engine import score
router=APIRouter()
class Location(BaseModel):
    latitude:float
    longitude:float
@router.post('/analyze')
def analyze(loc:Location):
    w=get_weather(loc.latitude,loc.longitude)
    return {'location':loc.model_dump(),'weather':w,**score(w)}
