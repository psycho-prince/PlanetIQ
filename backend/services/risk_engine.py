class RiskEngine:
    def calculate_fire_risk(self, temperature, humidity):
        """
        Simple fire risk index (0.0 to 1.0).
        High temp + Low humidity = High risk.
        """
        if temperature is None or humidity is None:
            return None
        
        # Simple heuristic: normalized risk score
        # Temp component: higher is worse (range 0-40C mapped to 0-0.6)
        # Humidity component: lower is worse (range 100-0% mapped to 0-0.4)
        
        temp_factor = min(max((temperature - 10) / 30, 0), 0.6)
        hum_factor = min(max((100 - humidity) / 100, 0), 0.4)
        
        return round(temp_factor + hum_factor, 2)

    def evaluate(self, health):
        return {"risk":"unknown"}
