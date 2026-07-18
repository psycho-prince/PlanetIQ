from typing import Dict, List


class FIRMSParser:

    @staticmethod
    def _to_float(value, default=0.0):
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _to_int(value, default=0):
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def parse_record(self, row: Dict) -> Dict:

        return {
            "latitude": self._to_float(row.get("latitude")),
            "longitude": self._to_float(row.get("longitude")),
            "brightness": self._to_float(
                row.get("bright_ti4")
                or row.get("brightness")
            ),
            "frp": self._to_float(row.get("frp")),
            "confidence": row.get("confidence", "unknown"),
            "acq_date": row.get("acq_date"),
            "acq_time": row.get("acq_time"),
            "satellite": row.get("satellite"),
            "instrument": row.get("instrument"),
            "daynight": row.get("daynight"),
        }

    def parse(self, rows: List[Dict]) -> List[Dict]:
        return [self.parse_record(row) for row in rows]


firms_parser = FIRMSParser()
