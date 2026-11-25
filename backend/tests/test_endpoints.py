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

def test_calculate_emissions_endpoint():
    payload = {
        "distance_km": 12.0,
        "car_speed_kmh": 20.0
    }
    response = client.post("/api/v1/calculate-emissions", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["distance_km"] == 12.0
    assert "baseline_ice_car_co2_kg" in data
    assert len(data["comparisons"]) == 4
    assert len(data["speed_emission_curve"]) > 5
    
    # Metro and Bus should show positive savings vs ICE car
    comp_map = {c["mode"]: c for c in data["comparisons"]}
    assert comp_map["Metro"]["savings_vs_ice_car_kg"] > 0
    assert comp_map["Metro"]["savings_percentage"] > 90.0

def test_congestion_emission_penalty_endpoint():
    payload = {
        "distance_km": 15.0,
        "actual_speed_kmh": 8.0,
        "free_flow_speed_kmh": 25.0
    }
    response = client.post("/api/v1/congestion-emission-penalty", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["actual_co2_kg"] > data["free_flow_co2_kg"]
    assert data["excess_congestion_co2_kg"] > 0
    assert data["congestion_penalty_percentage"] > 0

def test_commuter_emissions_projection_endpoint():
    payload = {
        "daily_roundtrip_km": 25.0,
        "working_days_per_week": 5,
        "chosen_mode": "Metro"
    }
    response = client.post("/api/v1/commuter-emissions-projection", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["annual_co2_saved_kg"] > 0
    assert data["annual_cost_saved_inr"] > 0
    assert data["annual_tree_years_equivalent"] > 0


def test_list_arai_profiles_endpoint():
    response = client.get("/api/v1/arai-profiles")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "petrol_small" in data["vehicle_profiles"]
    assert "ev_hatchback" in data["vehicle_profiles"]
    assert "bmtc_ebus" in data["vehicle_profiles"]
    assert "bmrcl_metro" in data["vehicle_profiles"]
    assert "karnataka_grid" in data["grid_regions_kg_co2_per_kwh"]


def test_vehicle_profile_emissions_endpoint():
    payload = {
        "profile_id": "bmtc_ebus",
        "distance_km": 12.0,
        "grid_region": "karnataka_grid",
        "occupancy_passengers": 45
    }
    response = client.post("/api/v1/vehicle-profile-emissions", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["mode"] == "Bus"
    assert data["total_co2_kg"] > 0
    assert len(data["modeling_notes"]) >= 1


def test_nearest_transit_stops_endpoint():
    response = client.get("/api/v1/transit-stops/nearest?lat=12.9756&lng=77.6066")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["nearest_metro_station"]["access_distance_km"] < 1.0
    assert data["indexed_bus_stops"] > 100


def test_door_to_door_emissions_endpoint():
    payload = {
        "origin": {"lat": 12.9784, "lng": 77.6408},
        "destination": {"lat": 12.9352, "lng": 77.6245},
        "car_speed_kmh": 18.0,
        "preferred_access_mode": "feeder_bus",
        "grid_region": "karnataka_grid"
    }
    response = client.post("/api/v1/door-to-door-emissions", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["door_to_door_comparison"]) == 4
    modes = {m["mode"]: m for m in data["door_to_door_comparison"]}
    assert modes["Metro"]["co2_saved_vs_car_kg"] > 0




