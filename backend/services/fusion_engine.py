from connectors.openmeteo import openmeteo_connector
from connectors.firms import firms_connector


class FusionEngine:

    def analyze(self, latitude: float, longitude: float):

        weather_result = openmeteo_connector.fetch(latitude, longitude)
        fire_result = firms_connector.fetch(latitude, longitude)

        weather = weather_result.get("data", {}) if weather_result.get("status") == "success" else {}
        fire = fire_result.get("data", {}) if fire_result.get("status") == "success" else {}

        temperature = weather.get("temperature")
        humidity = weather.get("humidity")
        precipitation = weather.get("precipitation")
        wind_speed = weather.get("wind_speed")

        hotspot_count = fire.get("hotspot_count", 0)
        hotspots = fire.get("hotspots", [])

        health = 100
        recommendations = []

        if temperature is not None:
            if temperature >= 45:
                health -= 35
                recommendations.append("Extreme heat detected.")
            elif temperature >= 40:
                health -= 20
                recommendations.append("Very high temperature detected.")
            elif temperature >= 35:
                health -= 10

        if precipitation is not None and precipitation > 50:
            health -= 5

        if wind_speed is not None and wind_speed > 50:
            health -= 10
            recommendations.append("Strong winds detected.")

        if hotspot_count:
            deduction = min(40, hotspot_count * 5)
            health -= deduction
            recommendations.append(
                f"{hotspot_count} wildfire hotspot(s) detected nearby."
            )

        health = max(0, min(100, health))

        if health >= 80:
            risk = "Low"
        elif health >= 60:
            risk = "Moderate"
        elif health >= 40:
            risk = "High"
        else:
            risk = "Critical"

        if not recommendations:
            recommendations.append(
                "No immediate environmental threats detected."
            )

        return {
            "location": {
                "latitude": latitude,
                "longitude": longitude,
            },
            "ecosystem_health": health,
            "risk": risk,
            "weather": {
                "temperature": temperature,
                "humidity": humidity,
                "precipitation": precipitation,
                "wind_speed": wind_speed,
            },
            "fire": {
                "hotspot_count": hotspot_count,
                "hotspots": hotspots,
            },
            "recommendations": recommendations,
        }


fusion_engine = FusionEngine()
