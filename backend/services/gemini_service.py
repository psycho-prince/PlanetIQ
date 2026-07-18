import json
import os

import requests
from dotenv import load_dotenv

# Load .env from backend directory
load_dotenv()


class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")

    def generate_summary(self, ecosystem_data: dict):

        if not self.api_key:
            return {
                "summary": "Gemini API key not configured.",
                "concerns": [],
                "recommendations": [],
            }

        prompt = f"""
You are PlanetIQ's AI Environmental Analyst.

Analyze the environmental conditions below.

Return ONLY valid JSON.

Schema:

{{
  "summary":"...",
  "concerns":[
    "...",
    "..."
  ],
  "recommendations":[
    "...",
    "..."
  ]
}}

Environmental Data:

{json.dumps(ecosystem_data, indent=2)}
"""

        url = (
            "https://generativelanguage.googleapis.com/v1beta/"
            "models/gemini-flash-latest:generateContent"
        )

        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": self.api_key,
        }

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        try:

            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=30,
            )

            response.raise_for_status()

            result = response.json()

            text = (
                result["candidates"][0]
                ["content"]["parts"][0]["text"]
            )

            # Remove markdown if Gemini wraps JSON
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

            try:
                return json.loads(text)

            except Exception:
                return {
                    "summary": text,
                    "concerns": [],
                    "recommendations": [],
                }

        except Exception as e:

            return {
                "summary": f"Gemini API Error: {str(e)}",
                "concerns": [],
                "recommendations": [],
            }


gemini_service = GeminiService()
