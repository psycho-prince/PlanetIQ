import csv
import io
import requests

from core.config import settings


class FireService:

    BASE_URL = "https://firms.modaps.eosdis.nasa.gov/api/area/csv"

    DATASETS = [
        "VIIRS_NOAA21_NRT",
        "VIIRS_NOAA20_NRT",
        "VIIRS_SNPP_NRT",
        "MODIS_NRT",
    ]

    def get_hotspots(
        self,
        latitude: float,
        longitude: float,
        radius: float = 0.5,
        days: int = 1,
    ):

        west = longitude - radius
        east = longitude + radius
        south = latitude - radius
        north = latitude + radius

        bbox = f"{west},{south},{east},{north}"

        debug = []

        for dataset in self.DATASETS:

            url = (
                f"{self.BASE_URL}/"
                f"{settings.FIRMS_API_KEY}/"
                f"{dataset}/"
                f"{bbox}/"
                f"{days}"
            )

            try:

                response = requests.get(url, timeout=20)

                debug.append({
                    "dataset": dataset,
                    "status": response.status_code
                })

                response.raise_for_status()

                rows = list(
                    csv.DictReader(
                        io.StringIO(response.text)
                    )
                )

                if rows:

                    return {
                        "source": "NASA FIRMS",
                        "dataset": dataset,
                        "nearby_hotspots": len(rows),
                        "hotspots": rows[:20],
                        "datasets_checked": debug,
                        "status": "success",
                    }

            except Exception as e:

                debug.append({
                    "dataset": dataset,
                    "error": str(e)
                })

        return {
            "source": "NASA FIRMS",
            "dataset": None,
            "nearby_hotspots": 0,
            "hotspots": [],
            "datasets_checked": debug,
            "status": "success",
        }


fire_service = FireService()
