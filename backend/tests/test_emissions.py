import pytest
from app.services.emission_calculator import (
    haversine_distance_km,
    calculate_arai_emission_factor,
    calculate_weather_adjusted_emission_factor,
    calculate_congestion_emission_penalty,
    calculate_carbon_offset_impact,
    simulate_commuter_annual_savings,
    calculate_trip_emissions,
    calculate_modal_emissions_comparison,
    generate_speed_emission_curve,
    calculate_mode_duration,
    calculate_mode_cost,
    compute_all_routes_and_scores,
    ARAI_COEFFICIENTS
)

def test_haversine_distance_known_coordinates():
    # MG Road to Indiranagar (~4.0 to 5.5 km in Bengaluru)
    lat1, lon1 = 12.9756, 77.6066
    lat2, lon2 = 12.9784, 77.6408
    dist = haversine_distance_km(lat1, lon1, lat2, lon2)
    assert 3.0 <= dist <= 6.0

def test_haversine_distance_symmetry_and_zero():
    assert haversine_distance_km(12.97, 77.59, 12.97, 77.59) == 0.0
    d1 = haversine_distance_km(12.97, 77.59, 12.92, 77.62)
    d2 = haversine_distance_km(12.92, 77.62, 12.97, 77.59)
    assert d1 == d2

def test_arai_emission_factor_ice_car_speed_dependence():
    # Stop-and-go congestion (10 km/h) vs standard urban cruising speed (25 km/h)
    ef_congested = calculate_arai_emission_factor("ICE_Car", 10.0)
    ef_urban = calculate_arai_emission_factor("ICE_Car", 25.0)
    
    # 10 km/h: 140 + 350/10 + 0.02*100 = 177.0 g/km
    assert ef_congested == pytest.approx(177.0, rel=1e-2)
    # 25 km/h: 140 + 350/25 + 0.02*625 = 166.5 g/km
    assert ef_urban == pytest.approx(166.5, rel=1e-2)
    # Stop-and-go congestion produces significantly higher emissions than optimal urban cruising
    assert ef_congested > ef_urban

def test_arai_emission_factor_clamping():
    # Speeds <= 0 should clamp to minimum 5.0 km/h to prevent ZeroDivisionError
    ef_zero = calculate_arai_emission_factor("ICE_Car", 0.0)
    ef_negative = calculate_arai_emission_factor("ICE_Car", -15.0)
    ef_clamped = calculate_arai_emission_factor("ICE_Car", 5.0)
    
    assert ef_zero == ef_clamped
    assert ef_negative == ef_clamped

def test_modal_emission_hierarchy():
    distance_km = 10.0
    car_time_min = 30.0
    routes = compute_all_routes_and_scores(distance_km, car_time_min)
    
    co2_by_mode = {r["mode"]: r["co2_emissions_kg"] for r in routes}
    
    # Metro has lowest carbon per passenger, ICE Car has highest
    assert co2_by_mode["Metro"] < co2_by_mode["Bus"]
    assert co2_by_mode["Bus"] < co2_by_mode["EV"]
    assert co2_by_mode["EV"] < co2_by_mode["ICE_Car"]

def test_calculate_trip_emissions():
    res = calculate_trip_emissions("Metro", distance_km=15.0, speed_kmh=35.0)
    assert res["mode"] == "Metro"
    assert res["emission_factor_g_km"] == 12.0
    assert res["co2_emissions_kg"] == round(15.0 * 12.0 / 1000.0, 3)

def test_calculate_modal_emissions_comparison():
    res = calculate_modal_emissions_comparison(distance_km=10.0, car_speed_kmh=25.0)
    assert "comparisons" in res
    assert len(res["comparisons"]) == 4
    
    # Check that Metro and Bus show high percentage savings
    mode_savings = {c["mode"]: c["savings_percentage"] for c in res["comparisons"]}
    assert mode_savings["Metro"] > 90.0  # >90% carbon savings vs car
    assert mode_savings["Bus"] > 80.0

def test_speed_emission_curve_trend():
    curve = generate_speed_emission_curve()
    assert len(curve) > 5
    # Speed at 10 km/h (severe traffic) should have higher emission factor than speed at 25 km/h
    ef_10 = next(p["emission_factor_g_km"] for p in curve if p["speed_kmh"] == 10.0)
    ef_25 = next(p["emission_factor_g_km"] for p in curve if p["speed_kmh"] == 25.0)
    assert ef_10 > ef_25

def test_cost_calculation_and_caps():
    metro_cost_50km = calculate_mode_cost("Metro", 50.0)
    bus_cost_50km = calculate_mode_cost("Bus", 50.0)
    
    # BMTC maximum fare cap is ₹35, Namma Metro cap is ₹60
    assert metro_cost_50km <= 60.0
    assert bus_cost_50km <= 35.0

def test_recommendation_scoring_bounds_and_order():
    distance_km = 8.5
    car_time_min = 28.0
    routes = compute_all_routes_and_scores(distance_km, car_time_min)
    
    assert len(routes) == 4
    for r in routes:
        assert 0.0 <= r["recommendation_score"] <= 100.0
        assert r["duration_min"] > 0
        assert r["co2_emissions_kg"] >= 0
        assert r["estimated_cost_inr"] >= 0

    scores = [r["recommendation_score"] for r in routes]
    assert scores == sorted(scores, reverse=True)

def test_weather_adjusted_emission_factor():
    base_ef = calculate_arai_emission_factor("ICE_Car", 25.0)
    rainy_ef = calculate_weather_adjusted_emission_factor("ICE_Car", 25.0, rainfall_mm=10.0)
    # Heavy rainfall increases rolling resistance & wiper/defogger loads -> higher emissions
    assert rainy_ef > base_ef
    
    # Metro on dedicated track has 0 rain rolling friction penalty
    metro_base = calculate_arai_emission_factor("Metro", 35.0)
    metro_rain = calculate_weather_adjusted_emission_factor("Metro", 35.0, rainfall_mm=10.0)
    assert metro_base == metro_rain

def test_congestion_emission_penalty():
    # 10 km commute in Bengaluru traffic: 8 km/h severe gridlock vs 25 km/h optimal urban flow
    res = calculate_congestion_emission_penalty(distance_km=10.0, actual_speed_kmh=8.0, free_flow_speed_kmh=25.0)
    assert res["actual_co2_kg"] > res["free_flow_co2_kg"]
    assert res["excess_congestion_co2_kg"] > 0
    assert res["congestion_penalty_percentage"] > 0

def test_carbon_offset_impact():
    # If 10 kg of CO2 is saved
    offsets = calculate_carbon_offset_impact(10.0)
    assert offsets["tree_days_equivalent"] > 0
    assert offsets["fuel_saved_liters"] > 0
    assert offsets["smartphone_charges_equivalent"] > 0

def test_simulate_commuter_annual_savings():
    # 20 km daily roundtrip, 5 days a week using Metro
    sim = simulate_commuter_annual_savings(daily_roundtrip_distance_km=20.0, days_per_week=5, chosen_mode="Metro")
    assert sim["annual_co2_saved_kg"] > 500.0  # Massive annual carbon reduction
    assert sim["annual_cost_saved_inr"] > 10000.0 # Significant financial savings vs car
    assert sim["annual_tree_years_equivalent"] > 20.0

