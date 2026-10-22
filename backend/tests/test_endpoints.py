import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.xgboost_predictor import (
    predict_travel_time,
    predict_weather_adjusted_travel_time
)
from app.api.endpoints import haversine_distance

client = TestClient(app)

def test_haversine_distance():
    # MG Road to Indiranagar
    d = haversine_distance(12.9756, 77.6066, 12.9784, 77.6408)
    assert 3.0 <= d <= 6.0
    # Same coordinates must be 0.0
    assert haversine_distance(12.97, 77.59, 12.97, 77.59) == 0.0

def test_weather_adjusted_travel_time_regression():
    features = {
        'latitude': 12.9716,
        'longitude': 77.5946,
        'hour': 9,
        'day_of_week': 2,
        'is_peak_hour': 1
    }
    # Clear weather
    res_clear = predict_weather_adjusted_travel_time(features, rainfall_mm=0.0, distance_km=5.0)
    # Heavy rainfall (10 mm)
    res_rain = predict_weather_adjusted_travel_time(features, rainfall_mm=10.0, distance_km=5.0)
    
    assert res_clear["weather_adjusted_travel_time_min"] > 0
    assert res_rain["weather_adjusted_travel_time_min"] > res_clear["weather_adjusted_travel_time_min"]
    assert res_rain["weather_delay_min"] > 0

def test_health_check_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "running smoothly" in data["message"]

def test_predict_traffic_endpoint():
    payload = {
        "latitude": 12.9784,
        "longitude": 77.6408,
        "departure_time": "2026-10-15T09:00:00",
        "distance_km": 7.5,
        "rainfall_mm": 4.5
    }
    response = client.post("/api/v1/predict-traffic", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["weather_adjusted_travel_time_min"] > 0
    assert data["weather_delay_min"] >= 0
    assert data["is_peak_hour"] is True

def test_recommend_route_endpoint_contract():
    payload = {
        "origin": {"lat": 12.9716, "lng": 77.5946},
        "destination": {"lat": 12.9352, "lng": 77.6245},
        "intended_departure": "2026-10-15T08:30:00"
    }
    response = client.post("/api/v1/recommend-route", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["distance_km"] > 0
    assert len(data["routes"]) == 4
    assert "shap_explanation" in data
