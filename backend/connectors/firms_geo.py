import math
from typing import Dict, List, Optional


class FIRMSGeo:

    EARTH_RADIUS_KM = 6371.0

    def haversine(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float,
    ) -> float:

        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1)
            * math.cos(lat2)
            * math.sin(dlon / 2) ** 2
        )

        c = 2 * math.atan2(
            math.sqrt(a),
            math.sqrt(1 - a),
        )

        return self.EARTH_RADIUS_KM * c

    def nearest_hotspot(
        self,
        latitude: float,
        longitude: float,
        hotspots: List[Dict],
    ) -> Optional[Dict]:

        if not hotspots:
            return None

        nearest = None
        min_distance = float("inf")

        for hotspot in hotspots:

            distance = self.haversine(
                latitude,
                longitude,
                hotspot["latitude"],
                hotspot["longitude"],
            )

            hotspot["distance_km"] = round(distance, 2)

            if distance < min_distance:
                min_distance = distance
                nearest = hotspot

        return nearest

    def hotspots_within_radius(
        self,
        latitude: float,
        longitude: float,
        hotspots: List[Dict],
        radius_km: float,
    ) -> List[Dict]:

        results = []

        for hotspot in hotspots:

            distance = self.haversine(
                latitude,
                longitude,
                hotspot["latitude"],
                hotspot["longitude"],
            )

            if distance <= radius_km:

                hotspot["distance_km"] = round(distance, 2)
                results.append(hotspot)

        return results


firms_geo = FIRMSGeo()
