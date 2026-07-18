from typing import Optional

import requests

from backend.core.config import settings


class WeatherService:
    def __init__(self):
        self.base_url = settings.OPEN_METEO_URL

    def get_current_weather(
        self,
        latitude: float,
        longitude: float,
    ) -> dict:

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation",
                "wind_speed_10m"
            ]
        }

        try:
            response = requests.get(
                self.base_url,
                params=params,
                timeout=15,
            )

            response.raise_for_status()

            data = response.json()

            current = data.get("current", {})

            return {
                "temperature": current.get("temperature_2m"),
                "humidity": current.get("relative_humidity_2m"),
                "precipitation": current.get("precipitation"),
                "wind_speed": current.get("wind_speed_10m"),
                "status": "success",
            }

        except requests.exceptions.Timeout:
            return self._error("Request timed out")

        except requests.exceptions.ConnectionError:
            return self._error("Connection failed")

        except requests.exceptions.HTTPError as e:
            return self._error(str(e))

        except Exception as e:
            return self._error(str(e))

    def _error(self, message: str):
        return {
            "temperature": None,
            "humidity": None,
            "precipitation": None,
            "wind_speed": None,
            "status": "error",
            "message": message,
        }


weather_service = WeatherService()
