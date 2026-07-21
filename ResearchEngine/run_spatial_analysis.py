from PlanetIQ.backend.app.services.weather_service import get_weather
from PlanetIQ.backend.services.risk_engine import RiskEngine
from PlanetIQ.backend.services.alert_engine import AlertEngine

def run_spatial_fire_analysis(locations):
    risk_engine = RiskEngine()
    alert_engine = AlertEngine()
    
    print("--- Starting Spatial Fire Risk Analysis ---")
    for name, (lat, lon) in locations.items():
        weather = get_weather(lat, lon)
        risk = risk_engine.calculate_fire_risk(weather.get('temperature'), weather.get('humidity'))
        
        if risk is not None:
            print(f"Location: {name} | Risk: {risk}")
            alert_engine.check_and_alert(name, risk)
        else:
            print(f"Location: {name} | Risk: Unknown (Weather data unavailable)")

if __name__ == "__main__":
    test_locations = {
        "California": (36.7783, -119.4179),
        "Sydney": (-33.8688, 151.2093),
        "Amazon": (-3.4653, -62.2159)
    }
    run_spatial_fire_analysis(test_locations)
