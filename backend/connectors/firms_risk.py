from typing import Dict, List


class FIRMSRisk:

    def calculate(self, hotspots: List[Dict]) -> Dict:

        if not hotspots:
            return {
                "score": 0,
                "level": "Low",
                "reason": "No nearby hotspots detected."
            }

        score = 0

        for hotspot in hotspots:

            distance = hotspot.get("distance_km", 1000)
            frp = hotspot.get("frp", 0)

            if distance <= 5:
                score += 40
            elif distance <= 10:
                score += 25
            elif distance <= 25:
                score += 10

            if frp >= 100:
                score += 30
            elif frp >= 50:
                score += 20
            elif frp >= 10:
                score += 10

            confidence = str(
                hotspot.get("confidence", "")
            ).lower()

            if confidence in ("high", "h", "nominal"):
                score += 10

        score = min(score, 100)

        if score >= 80:
            level = "Critical"
        elif score >= 60:
            level = "High"
        elif score >= 30:
           
