import csv
import io
import requests

from backend.core.config import settings


class FireService:
    BASE_URL = "https://firms.modaps.eosdis.nasa.gov/api/area/csv"

    DATASETS = [
        "VIIRS_SNPP_NRT",
        "VIIRS_NOAA20_NRT",
        "VIIRS_NOAA21_NRT",
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
        south = latitude - radius
        east = longitude + radius
        north = latitude + radius

        bbox = f"{west},{south},{east},{north}"

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

                print("=" * 60)
                print("Dataset :", dataset)
                print("URL     :", url)
                print("Status  :", response.status_code)
                print("Preview :")
                print(response.text[:500])
                print("=" * 60)

                response.raise_for_status()

                rows = list(csv.DictReader(io.StringIO(response.text)))

                if len(rows) > 0:
                    return {
                        "source": "NASA FIRMS",
                        "dataset": dataset,
                        "nearby_hotspots": len(rows),
                        "hotspots": rows[:20],
                        "status": "success",
                    }

            except Exception as e:
                print(f"{dataset} failed -> {e}")

        return {
            "source": "NASA FIRMS",
            "dataset": None,
            "nearby_hotspots": 0,
            "hotspots": [],
            "status": "success",
        }


fire_service = FireService()
