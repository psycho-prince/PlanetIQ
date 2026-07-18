import requests

from backend.connectors.base import BaseConnector
from backend.core.config import settings


class OpenMeteoConnector(BaseConnector):

    def __init__(self):
        super().__init__("Open-Meteo")

    def fetch(self, latitude: float, longitude: float):

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation",
                "wind_speed_10m",
            ],
        }

        try:

            response = requests.get(
                settings.OPEN_METEO_URL,
                params=params,
                timeout=20,
            )

            response.raise_for_status()

            current = response.json()["current"]

            return self.success({
                "temperature": current["temperature_2m"],
                "humidity": current["relative_humidity_2m"],
                "precipitation": current["precipitation"],
                "wind_speed": current["wind_speed_10m"],
            })

        except Exception as e:

            return self.error(str(e))

    def health_check(self):

        try:

            response = requests.get(
                "https://api.open-meteo.com",
                timeout=5,
            )

            return response.status_code == 200

        except Exception:

            return False


openmeteo_connector = OpenMeteoConnector()
