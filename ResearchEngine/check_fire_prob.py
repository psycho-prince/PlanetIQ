from PlanetIQ.backend.app.services.weather_service import get_weather
from PlanetIQ.backend.services.risk_engine import RiskEngine

def get_fire_probability(lat, lon):
    # 1. Fetch current weather
    weather = get_weather(lat, lon)
    
    # 2. Calculate risk
    engine = RiskEngine()
    risk = engine.calculate_fire_risk(weather['temperature'], weather['humidity'])
    
    return {
        "latitude": lat,
        "longitude": lon,
        "weather": weather,
        "fire_risk_score": risk
    }

if __name__ == "__main__":
    # Test for a location (e.g., California)
    lat, lon = 36.7783, -119.4179
    result = get_fire_probability(lat, lon)
    print(f"Fire Probability Analysis: {result}")
