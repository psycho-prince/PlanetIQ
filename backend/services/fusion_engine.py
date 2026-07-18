from connectors.openmeteo import openmeteo_connector
from connectors.firms import firms_connector
from services.gemini_service import gemini_service


class FusionEngine:

    def analyze(self, latitude: float, longitude: float):

        weather_result = openmeteo_connector.fetch(latitude, longitude)
        fire_result = firms_connector.fetch(latitude, longitude)

        weather = (
            weather_result.get("data", {})
            if weather_result.get("status") == "success"
            else {}
        )

        fire = (
            fire_result.get("data", {})
            if fire_result.get("status") == "success"
            else {}
        )

        temperature = weather.get("temperature")
        humidity = weather.get("humidity")
        precipitation = weather.get("precipitation")
        wind_speed = weather.get("wind_speed")

        hotspot_count = fire.get("hotspot_count", 0)
        hotspots = fire.get("hotspots", [])

        health = 100
        recommendations = []

        # ------------------------
        # Temperature
        # ------------------------

        if temperature is not None:

            if temperature >= 45:
                health -= 35
                recommendations.append(
                    "Extreme heat detected."
                )

            elif temperature >= 40:
                health -= 20
                recommendations.append(
                    "Very high temperature detected."
                )

            elif temperature >= 35:
                health -= 10

        # ------------------------
        # Rain
        # ------------------------

        if precipitation is not None:

            if precipitation > 50:
                health -= 5

        # ------------------------
        # Wind
        # ------------------------

        if wind_speed is not None:

            if wind_speed > 50:
                health -= 10
                recommendations.append(
                    "Strong winds detected."
                )

        # ------------------------
        # Fire
        # ------------------------

        if hotspot_count:

            deduction = min(
                40,
                hotspot_count * 5,
            )

            health -= deduction

            recommendations.append(
                f"{hotspot_count} wildfire hotspot(s) detected nearby."
            )

        # ------------------------
        # Clamp
        # ------------------------

        health = max(
            0,
            min(
                100,
                health,
            ),
        )

        # ------------------------
        # Risk
        # ------------------------

        if health >= 80:
            risk = "Low"

        elif health >= 60:
            risk = "Moderate"

        elif health >= 40:
            risk = "High"

        else:
            risk = "Critical"

        # ------------------------
        # Default recommendation
        # ------------------------

        if not recommendations:

            recommendations.append(
                "No immediate environmental threats detected."
            )

        # ------------------------
        # Gemini AI
        # ------------------------

        ai_summary = gemini_service.generate_summary(
            {
                "location": {
                    "latitude": latitude,
                    "longitude": longitude,
                },
                "ecosystem_health": health,
                "risk": risk,
                "temperature": temperature,
                "humidity": humidity,
                "precipitation": precipitation,
                "wind_speed": wind_speed,
                "fire_hotspots": hotspot_count,
                "recommendations": recommendations,
            }
        )

        # ------------------------
        # Response
        # ------------------------

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

            "ai_summary": ai_summary,
        }


fusion_engine = FusionEngine()
