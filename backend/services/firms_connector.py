import csv
import io
import logging
from typing import Dict, List

import requests

from backend.core.config import settings


class FIRMSConnector:
    BASE_URL = "https://firms.modaps.eosdis.nasa.gov/api/area/csv"

    DATASETS = [
        "VIIRS_NOAA21_NRT",
        "VIIRS_NOAA20_NRT",
        "VIIRS_SNPP_NRT",
        "MODIS_NRT",
    ]

    def __init__(self):
        self.session = requests.Session()

    def _bbox(self, lat: float, lon: float, radius: float):
        return (
            lon - radius,
            lat - radius,
            lon + radius,
            lat + radius,
        )

    def _build_url(
        self,
        dataset: str,
        lat: float,
        lon: float,
        radius: float,
        days: int,
    ):

        west, south, east, north = self._bbox(lat, lon, radius)

        bbox = f"{west},{south},{east},{north}"

        return (
            f"{self.BASE_URL}/"
            f"{settings.FIRMS_API_KEY}/"
            f"{dataset}/"
            f"{bbox}/"
            f"{days}"
        )

    def query_dataset(
        self,
        dataset: str,
        lat: float,
        lon: float,
        radius: float = 1.0,
        days: int = 1,
    ) -> List[Dict]:

        url = self._build_url(dataset, lat, lon, radius, days)

        response = self.session.get(url, timeout=30)

        logging.info(url)

        response.raise_for_status()

        rows = list(csv.DictReader(io.StringIO(response.text)))

        return rows

    def search(
        self,
        latitude: float,
        longitude: float,
        radius: float = 1.0,
        days: int = 1,
    ):

        debug = []

        for dataset in self.DATASETS:

            try:

                rows = self.query_dataset(
                    dataset,
                    latitude,
                    longitude,
                    radius,
                    days,
                )

                debug.append(
                    {
                        "dataset": dataset,
                        "records": len(rows),
                    }
                )

                if rows:

                    return {
                        "success": True,
                        "dataset": dataset,
                        "count": len(rows),
                        "records": rows,
                        "debug": debug,
                    }

            except Exception as e:

                debug.append(
                    {
                        "dataset": dataset,
                        "error": str(e),
                    }
                )

        return {
            "success": True,
            "dataset": None,
            "count": 0,
            "records": [],
            "debug": debug,
        }


firms_connector = FIRMSConnector()
