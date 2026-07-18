import csv
import io
import requests

from core.config import settings


class FIRMSAreaAPI:
    BASE_URL = "https://firms.modaps.eosdis.nasa.gov/api/area/csv"

    def __init__(self):
        self.session = requests.Session()

    def build_bbox(
        self,
        latitude: float,
        longitude: float,
        radius: float = 0.5,
    ) -> str:

        west = longitude - radius
        south = latitude - radius
        east = longitude + radius
        north = latitude + radius

        return f"{west},{south},{east},{north}"

    def fetch(
        self,
        dataset: str,
        latitude: float,
        longitude: float,
        radius: float = 0.5,
        days: int = 1,
    ):

        bbox = self.build_bbox(
            latitude,
            longitude,
            radius,
        )

        url = (
            f"{self.BASE_URL}/"
            f"{settings.FIRMS_API_KEY}/"
            f"{dataset}/"
            f"{bbox}/"
            f"{days}"
        )

        response = self.session.get(
            url,
            timeout=30,
        )

        response.raise_for_status()

        rows = list(
            csv.DictReader(
                io.StringIO(response.text)
            )
        )

        return {
            "dataset": dataset,
            "bbox": bbox,
            "records": rows,
            "count": len(rows),
            "url": url,
        }


firms_area = FIRMSAreaAPI()
