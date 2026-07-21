#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "Creating PlanetIQ backend..."

mkdir -p backend/app/{routers,services,schemas,models,utils}

touch backend/__init__.py
touch backend/app/__init__.py
touch backend/app/routers/__init__.py
touch backend/app/services/__init__.py
touch backend/app/schemas/__init__.py
touch backend/app/models/__init__.py
touch backend/app/utils/__init__.py

cat > backend/app/config.py << 'EOF'
from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = os.getenv("APP_NAME","PlanetIQ")
DEBUG = os.getenv("DEBUG","True") == "True"
EOF

cat > backend/app/schemas/request.py << 'EOF'
from pydantic import BaseModel

class Location(BaseModel):
    latitude: float
    longitude: float
EOF

cat > backend/app/schemas/response.py << 'EOF'
from pydantic import BaseModel

class AnalysisResponse(BaseModel):
    latitude: float
    longitude: float
    weather: dict
    ecosystem_health: int
    risk: str
EOF

cat > backend/app/services/weather_service.py << 'EOF'
import requests

def get_weather(lat, lon):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m"
    )

    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        current = r.json()["current"]

        return {
            "temperature": current["temperature_2m"],
            "humidity": current["relative_humidity_2m"]
        }

    except Exception:
        return {
            "temperature": None,
            "humidity": None
        }
EOF

cat > backend/app/services/health_engine.py << 'EOF'
def calculate_health(weather):

    if weather["temperature"] is None:
        return 50, "Unknown"

    score = 100

    if weather["temperature"] > 35:
        score -= 20

    if weather["humidity"] < 30:
        score -= 10

    if score >= 80:
        risk = "Low"
    elif score >= 60:
        risk = "Medium"
    else:
        risk = "High"

    return score, risk
EOF

cat > backend/app/main.py << 'EOF'
from fastapi import FastAPI

from backend.app.schemas.request import Location
from backend.app.schemas.response import AnalysisResponse

from backend.app.services.weather_service import get_weather
from backend.app.services.health_engine import calculate_health

app = FastAPI(
    title="PlanetIQ",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "project":"PlanetIQ",
        "status":"Running"
    }

@app.post("/analyze", response_model=AnalysisResponse)
def analyze(location: Location):

    weather = get_weather(location.latitude, location.longitude)

    score, risk = calculate_health(weather)

    return AnalysisResponse(
        latitude=location.latitude,
        longitude=location.longitude,
        weather=weather,
        ecosystem_health=score,
        risk=risk
    )
EOF

cat > backend/requirements.txt << 'EOF'
fastapi
uvicorn
requests
python-dotenv
pydantic
EOF

echo ""
echo "======================================="
echo "PlanetIQ backend generated successfully"
echo "======================================="
echo ""
echo "Install:"
echo "pip install -r backend/requirements.txt"
echo ""
echo "Run:"
echo "uvicorn backend.app.main:app --reload"
