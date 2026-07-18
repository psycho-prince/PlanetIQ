from backend.connectors.openmeteo import openmeteo_connector
from backend.connectors.firms import firms_connector


class FusionEngine:

    def analyze(
        self,
        latitude: float,
        longitude: float,
    ):

        weather = openmeteo_connector.fetch(
            latitude,
            longitude,
        )

        fire = firms_connector.fetch(
            latitude,
            longitude,
        )

        weather_data = weather.get("data", {})
        fire_data = fire.get("data", {})

        health = 100

        recommendations = []

        # Weather scoring
        temperature = weather_data.get("temperature")

        if temperature is not None:
            if temperature > 40:
                health -= 20
                recommendations.append(
                    "Extreme temperature detected."
                )
            elif temperature > 35:
                health -= 10

        precipitation = weather_data.get("precipitation")

        if precipitation is not None:
            if precipitation > 40:
                health -= 5

        # Fire scoring (placeholder until hotspot query is complete)
        hotspot_count = fire_data.get("hotspot_count", 0)

        if hotspot_count > 0:
            health -= min(40, hotspot_count * 5)
            recommendations.append(
                "Nearby wildfire activity detected."
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
            "weather": weather,
            "fire": fire,
            "ecosystem_health": health,
            "risk": risk,
            "recommendations": recommendations,
        }


fusion_engine = FusionEngine()
