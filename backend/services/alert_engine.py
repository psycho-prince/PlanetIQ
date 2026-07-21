class AlertEngine:
    def check_and_alert(self, location_name, risk_score):
        """Triggers alerts if risk score exceeds threshold."""
        threshold = 0.8
        if risk_score >= threshold:
            print(f"ALERT: High fire risk at {location_name}! Score: {risk_score}")
            return True
        return False
