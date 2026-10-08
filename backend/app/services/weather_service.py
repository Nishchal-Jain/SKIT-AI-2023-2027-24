import os
import requests
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "dummy_key_for_now")

def fetch_live_weather(lat: float, lon: float) -> Dict[str, str | float]:
    """
    Fetches real-time weather telemetry from OpenWeather API for given coordinates.
    Implements a fallback mechanism if the API times out (per NFR-002).
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    
    try:
        response = requests.get(url, timeout=3.0) # NFR-002 strict timeout
        response.raise_for_status()
        data = response.json()
        
        # Parse OpenWeather format
        condition = data["weather"][0]["main"]
        temp = data["main"]["temp"]
        rain = data.get("rain", {}).get("1h", 0.0) # mm in last 1 hour
        
        return {
            "condition": condition,
            "rainfall_mm": rain,
            "temperature_c": temp
        }
        
    except requests.exceptions.RequestException:
        # NFR-002 Fallback defaults if API fails
        print("Warning: OpenWeather API unreachable. Falling back to seasonal averages.")
        return {
            "condition": "Clear",
            "rainfall_mm": 0.0,
            "temperature_c": 28.5
        }
