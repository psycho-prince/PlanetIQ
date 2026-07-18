import csv
import io
import requests

from backend.connectors.base import BaseConnector
from backend.core.config import settings


class FIRMSConnector(BaseConnector):

    BASE_URL = "https://firms.modaps.eosdis.nasa.gov/api"

    def __init__(self):
        super().__init__("NASA FIRMS")
        self.session = requests.Session()

    def health_check(self) -> bool:
        try:
            r = self.session.get(
                f"{self.BASE_URL}/data_availability/csv/{settings.FIRMS_API_KEY}/ALL",
                timeout=10,
            )
            return r.status_code == 200
        except Exception:
            return False

    def available_datasets(self):

        url = (
            f"{self.BASE_URL}/data_availability/csv/"
            f"{settings.FIRMS_API_KEY}/ALL"
        )

        r = self.session.get(url, timeout=20)
        r.raise_for_status()

        rows = list(csv.DictReader(io.StringIO(r.text)))

        return rows

    def fetch(
        self,
        latitude: float,
        longitude: float,
        radius: float = 0.5,
        days: int = 1,
    ):

        try:

            datasets = self.available_datasets()

            return self.success({
                "latitude": latitude,
                "longitude": longitude,
                "radius": radius,
                "days": days,
                "available_datasets": datasets
            })

        except Exception as e:

            return self.error(str(e))


firms_connector = FIRMSConnector()
