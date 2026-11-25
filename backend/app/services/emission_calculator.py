import math
from typing import Dict, List, Any

# ARAI Standard Parameters & Emission Constants
# EF_CO2(v) = alpha + beta/v + gamma * v^2  (in grams CO2 per km)
ARAI_COEFFICIENTS = {
    "ICE_Car": {"alpha": 140.0, "beta": 350.0, "gamma": 0.02},
    "EV": {"fixed_factor": 123.0},       # Grid lifecycle factor: 0.82 kg CO2/kWh * 0.15 kWh/km
    "Bus": {"per_passenger": 20.0},      # 800 g/km fleet average / 40 passengers
    "Metro": {"per_passenger": 12.0}     # Dedicated electrified mass transit
}

# Granular ARAI BS-VI Sub-Classes, CEA Grid Carbon Intensities & Transit Fleets (Sprint 2)
GRID_CARBON_INTENSITY = {
    "india_cea_national": 0.82,   # kg CO2/kWh (CEA India National Grid average)
    "karnataka_grid": 0.58,       # kg CO2/kWh (BESCOM / Karnataka renewable + thermal mix)
    "rooftop_solar": 0.05         # kg CO2/kWh (Lifecycle solar PV charging)
}

ARAI_VEHICLE_PROFILES = {
    # --- Cars (BS-VI Speed-Dependent Polynomials: alpha + beta/v + gamma*v^2) ---
    "petrol_small": {
        "mode": "ICE_Car",
        "label": "Hatchback Petrol (<1200cc BS-VI)",
        "alpha": 125.0, "beta": 310.0, "gamma": 0.018,
        "supports_cold_start": True
    },
    "petrol_sedan_suv": {
        "mode": "ICE_Car",
        "label": "Sedan / SUV Petrol (>1200cc BS-VI)",
        "alpha": 158.0, "beta": 390.0, "gamma": 0.024,
        "supports_cold_start": True
    },
    "diesel_car": {
        "mode": "ICE_Car",
        "label": "Diesel Car (BS-VI)",
        "alpha": 132.0, "beta": 290.0, "gamma": 0.017,
        "supports_cold_start": True
    },
    "cng_car": {
        "mode": "ICE_Car",
        "label": "CNG Bi-Fuel Car (BS-VI)",
        "alpha": 104.0, "beta": 240.0, "gamma": 0.014,
        "supports_cold_start": True
    },
    "hybrid_car": {
        "mode": "ICE_Car",
        "label": "Strong Hybrid Car (HEV)",
        "alpha": 88.0, "beta": 160.0, "gamma": 0.012,
        "supports_cold_start": False
    },
    # --- Electric Vehicles (kWh/km x Grid Carbon Intensity + Regen Braking) ---
    "ev_two_wheeler": {
        "mode": "EV",
        "label": "Electric 2-Wheeler Scooter",
        "kwh_per_km": 0.032
    },
    "ev_hatchback": {
        "mode": "EV",
        "label": "Compact Electric Hatchback",
        "kwh_per_km": 0.130
    },
    "ev_sedan_suv": {
        "mode": "EV",
        "label": "Electric Sedan / SUV",
        "kwh_per_km": 0.180
    },
    # --- Buses (BMTC Fleet Categories with Passenger Occupancy Scaling) ---
    "bmtc_non_ac": {
        "mode": "Bus",
        "label": "BMTC Non-AC Diesel Bus",
        "fleet_g_km": 780.0,
        "nominal_passengers": 40
    },
    "bmtc_volvo_ac": {
        "mode": "Bus",
        "label": "BMTC Vajra Volvo AC Bus",
        "fleet_g_km": 960.0,
        "nominal_passengers": 38
    },
    "bmtc_ebus": {
        "mode": "Bus",
        "label": "BMTC Electric Bus (e-Bus)",
        "kwh_per_km": 0.95,
        "nominal_passengers": 40
    },
    # --- Metro (BMRCL Namma Metro Electrified Mass Transit) ---
    "bmrcl_metro": {
        "mode": "Metro",
        "label": "BMRCL Namma Metro (6-Coach Train)",
        "base_per_passenger_g_km": 12.0,
        "nominal_occupancy_ratio": 1.0
    },
    # --- First/Last-Mile Para-Transit Modes ---
    "auto_rickshaw_cng": {
        "mode": "Auto",
        "label": "CNG Auto-Rickshaw",
        "fixed_factor": 75.0
    },
    "ev_auto": {
        "mode": "Auto",
        "label": "Electric Auto-Rickshaw",
        "kwh_per_km": 0.055
    }
}

# Bengaluru Transit Kinematics & Operational Parameters
MODAL_PARAMS = {
    "Metro": {"speed_kmh": 35.0, "access_wait_min": 5.0, "base_fare": 10.0, "per_km_fare": 2.50, "max_fare": 60.0},
    "Bus": {"speed_kmh": 18.0, "access_wait_min": 3.0, "base_fare": 5.0, "per_km_fare": 2.00, "max_fare": 35.0},
    "EV": {"per_km_cost": 3.50},
    "ICE_Car": {"per_km_cost": 11.50}  # Petrol @ ~102/L, ~13 km/L mileage + maintenance
}

def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Computes great-circle distance between two GPS coordinates using Haversine formula.
    """
    R = 6371.0  # Earth's radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

def calculate_arai_emission_factor(mode: str, speed_kmh: float) -> float:
    """
    Calculates specific CO2 emission factor in grams CO2 per vehicle/passenger-km 
    using ARAI standard speed-dependent polynomial curves.
    
    Formula for ICE Car: EF(v) = 140 + 350/v + 0.02*v^2
    """
    effective_speed = max(speed_kmh, 5.0)  # Clamp lower bound to 5 km/h to prevent division by zero
    
    if mode == "ICE_Car":
        coeff = ARAI_COEFFICIENTS["ICE_Car"]
        return coeff["alpha"] + (coeff["beta"] / effective_speed) + (coeff["gamma"] * (effective_speed ** 2))
    elif mode == "EV":
        return ARAI_COEFFICIENTS["EV"]["fixed_factor"]
    elif mode == "Bus":
        return ARAI_COEFFICIENTS["Bus"]["per_passenger"]
    elif mode == "Metro":
        return ARAI_COEFFICIENTS["Metro"]["per_passenger"]
    else:
        raise ValueError(f"Unsupported transit mode: {mode}")

def calculate_weather_adjusted_emission_factor(
    mode: str,
    speed_kmh: float,
    rainfall_mm: float = 0.0,
    temperature_c: float = 25.0
) -> float:
    """
    Adjusts ARAI emission factors for real-world environmental conditions:
    1. Rainfall increases rolling friction and wiper/defogger auxiliary loads.
    2. Temperature extremes increase cabin HVAC energy consumption.
    3. Dedicated electrified Metro remains impervious to wet road friction.
    """
    base_factor = calculate_arai_emission_factor(mode, speed_kmh)
    
    rain_penalty = 0.0
    if rainfall_mm > 0.0:
        if mode == "ICE_Car":
            rain_penalty = min(rainfall_mm * 0.015, 0.18)
        elif mode == "EV":
            rain_penalty = min(rainfall_mm * 0.012, 0.15)
        elif mode == "Bus":
            rain_penalty = min(rainfall_mm * 0.008, 0.10)
        elif mode == "Metro":
            rain_penalty = 0.0
            
    temp_penalty = 0.0
    if temperature_c > 32.0:
        # High heat AC load penalty
        ac_multiplier = min((temperature_c - 32.0) * 0.01, 0.10)
        if mode in ["ICE_Car", "EV"]:
            temp_penalty = ac_multiplier
            
    total_multiplier = 1.0 + rain_penalty + temp_penalty
    return round(base_factor * total_multiplier, 2)

def calculate_congestion_emission_penalty(
    distance_km: float,
    actual_speed_kmh: float,
    free_flow_speed_kmh: float = 25.0
) -> Dict[str, Any]:
    """
    Quantifies excess vehicular CO2 emitted purely due to Bengaluru traffic gridlock
    compared to uninterrupted free-flow urban arterial driving.
    """
    safe_dist = max(distance_km, 0.5)
    actual_ef = calculate_arai_emission_factor("ICE_Car", actual_speed_kmh)
    free_flow_ef = calculate_arai_emission_factor("ICE_Car", free_flow_speed_kmh)
    
    congested_co2_kg = round((safe_dist * actual_ef) / 1000.0, 3)
    free_flow_co2_kg = round((safe_dist * free_flow_ef) / 1000.0, 3)
    excess_co2_kg = max(round(congested_co2_kg - free_flow_co2_kg, 3), 0.0)
    penalty_pct = round(((congested_co2_kg - free_flow_co2_kg) / free_flow_co2_kg) * 100.0, 1) if free_flow_co2_kg > 0 else 0.0
    
    return {
        "distance_km": round(safe_dist, 2),
        "actual_speed_kmh": round(actual_speed_kmh, 1),
        "free_flow_speed_kmh": round(free_flow_speed_kmh, 1),
        "actual_co2_kg": congested_co2_kg,
        "free_flow_co2_kg": free_flow_co2_kg,
        "excess_congestion_co2_kg": excess_co2_kg,
        "congestion_penalty_percentage": penalty_pct
    }

def calculate_carbon_offset_impact(co2_saved_kg: float) -> Dict[str, float]:
    """
    Translates raw carbon reduction (kg CO2) into tangible ecological equivalents:
    - Urban tree absorption days (average mature tree absorbs ~21.7 kg CO2/year ≈ 0.0595 kg/day).
    - Petrol fuel saved (liters) at ~2.31 kg CO2/liter.
    - Smartphone recharge cycles (~8.22 g CO2 per full charge).
    """
    safe_saved = max(co2_saved_kg, 0.0)
    return {
        "tree_days_equivalent": round(safe_saved / 0.0595, 1),
        "fuel_saved_liters": round(safe_saved / 2.31, 2),
        "smartphone_charges_equivalent": round((safe_saved * 1000.0) / 8.22, 0)
    }

def simulate_commuter_annual_savings(
    daily_roundtrip_distance_km: float,
    days_per_week: int = 5,
    chosen_mode: str = "Metro",
    car_speed_kmh: float = 25.0
) -> Dict[str, Any]:
    """
    Simulates cumulative weekly, monthly, and annual environmental and financial savings
    for a commuter choosing sustainable transit over a private ICE car in Bengaluru.
    """
    safe_dist = max(daily_roundtrip_distance_km, 1.0)
    safe_days = max(min(days_per_week, 7), 1)
    
    car_ef = calculate_arai_emission_factor("ICE_Car", car_speed_kmh)
    car_daily_co2 = (safe_dist * car_ef) / 1000.0
    car_daily_cost = safe_dist * MODAL_PARAMS["ICE_Car"]["per_km_cost"]
    
    transit_ef = calculate_arai_emission_factor(chosen_mode, MODAL_PARAMS[chosen_mode].get("speed_kmh", car_speed_kmh))
    transit_daily_co2 = (safe_dist * transit_ef) / 1000.0
    transit_daily_cost = calculate_mode_cost(chosen_mode, safe_dist / 2.0) * 2.0 # Round trip
    
    daily_co2_saved = max(car_daily_co2 - transit_daily_co2, 0.0)
    daily_cost_saved = max(car_daily_cost - transit_daily_cost, 0.0)
    
    working_weeks = 48 # Standard corporate working weeks per year
    annual_days = safe_days * working_weeks
    
    annual_co2_saved_kg = round(daily_co2_saved * annual_days, 1)
    annual_cost_saved_inr = round(daily_cost_saved * annual_days, 2)
    
    return {
        "chosen_mode": chosen_mode,
        "daily_roundtrip_km": round(safe_dist, 2),
        "working_days_per_week": safe_days,
        "annual_working_days": annual_days,
        "weekly_co2_saved_kg": round(daily_co2_saved * safe_days, 2),
        "monthly_co2_saved_kg": round(daily_co2_saved * safe_days * 4, 2),
        "annual_co2_saved_kg": annual_co2_saved_kg,
        "annual_cost_saved_inr": annual_cost_saved_inr,
        "annual_tree_years_equivalent": round(annual_co2_saved_kg / 21.7, 1),
        "annual_fuel_liters_saved": round(annual_co2_saved_kg / 2.31, 1)
    }

def calculate_trip_emissions(mode: str, distance_km: float, speed_kmh: float) -> Dict[str, Any]:
    """
    Calculates total CO2 emissions for a specific mode over a given distance.
    """
    factor = calculate_arai_emission_factor(mode, speed_kmh)
    co2_kg = round((distance_km * factor) / 1000.0, 3)
    return {
        "mode": mode,
        "distance_km": round(distance_km, 2),
        "speed_kmh": round(speed_kmh, 1),
        "emission_factor_g_km": round(factor, 2),
        "co2_emissions_kg": co2_kg
    }

def calculate_modal_emissions_comparison(distance_km: float, car_speed_kmh: float = 25.0) -> Dict[str, Any]:
    """
    Computes comparative emissions across all 4 modes (ICE Car, EV, Bus, Metro),
    quantifying absolute carbon savings and percentage reduction relative to private ICE car.
    """
    safe_dist = max(distance_km, 0.5)
    modes = ["ICE_Car", "EV", "Bus", "Metro"]
    comparison = []
    
    car_factor = calculate_arai_emission_factor("ICE_Car", car_speed_kmh)
    baseline_car_co2_kg = (safe_dist * car_factor) / 1000.0
    
    for mode in modes:
        speed = car_speed_kmh if mode in ["ICE_Car", "EV"] else MODAL_PARAMS[mode]["speed_kmh"]
        factor = calculate_arai_emission_factor(mode, speed)
        co2_kg = round((safe_dist * factor) / 1000.0, 3)
        savings_kg = round(max(baseline_car_co2_kg - co2_kg, 0.0), 3)
        savings_pct = round(((baseline_car_co2_kg - co2_kg) / baseline_car_co2_kg) * 100.0, 1) if baseline_car_co2_kg > 0 else 0.0
        
        comparison.append({
            "mode": mode,
            "speed_kmh": round(speed, 1),
            "emission_factor_g_km": round(factor, 2),
            "co2_emissions_kg": co2_kg,
            "savings_vs_ice_car_kg": savings_kg,
            "savings_percentage": savings_pct,
            "ecological_offset": calculate_carbon_offset_impact(savings_kg)
        })
        
    return {
        "distance_km": round(safe_dist, 2),
        "car_speed_kmh": round(car_speed_kmh, 1),
        "baseline_ice_car_co2_kg": round(baseline_car_co2_kg, 3),
        "comparisons": comparison
    }

def generate_speed_emission_curve(speed_range: List[float] = None) -> List[Dict[str, float]]:
    """
    Generates data points along the ARAI speed-emission curve for ICE Car (10 to 80 km/h),
    demonstrating how severe traffic congestion drastically elevates vehicle carbon intensity.
    """
    speeds = speed_range or [10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 50.0, 60.0, 70.0, 80.0]
    curve = []
    for s in speeds:
        ef = calculate_arai_emission_factor("ICE_Car", s)
        curve.append({
            "speed_kmh": s,
            "emission_factor_g_km": round(ef, 2)
        })
    return curve

def calculate_mode_duration(mode: str, distance_km: float, road_travel_time_min: float) -> float:
    """
    Calculates realistic mode duration (minutes) combining baseline model output
    and dedicated right-of-way transit kinematics.
    """
    if mode == "ICE_Car":
        return max(road_travel_time_min, 4.0)
    elif mode == "EV":
        return max(road_travel_time_min * 0.98, 4.0)
    elif mode == "Metro":
        run_time = (distance_km / MODAL_PARAMS["Metro"]["speed_kmh"]) * 60.0
        return round(run_time + MODAL_PARAMS["Metro"]["access_wait_min"], 1)
    elif mode == "Bus":
        run_time = (distance_km / MODAL_PARAMS["Bus"]["speed_kmh"]) * 60.0
        return round(run_time + MODAL_PARAMS["Bus"]["access_wait_min"], 1)
    else:
        return road_travel_time_min

def calculate_mode_cost(mode: str, distance_km: float) -> float:
    """
    Calculates estimated travel cost in Indian Rupees (INR) for Bengaluru.
    """
    if mode == "Metro":
        cfg = MODAL_PARAMS["Metro"]
        cost = cfg["base_fare"] + (distance_km * cfg["per_km_fare"])
        return round(min(cost, cfg["max_fare"]), 2)
    elif mode == "Bus":
        cfg = MODAL_PARAMS["Bus"]
        cost = cfg["base_fare"] + (distance_km * cfg["per_km_fare"])
        return round(min(cost, cfg["max_fare"]), 2)
    elif mode == "EV":
        return round(distance_km * MODAL_PARAMS["EV"]["per_km_cost"], 2)
    elif mode == "ICE_Car":
        return round(distance_km * MODAL_PARAMS["ICE_Car"]["per_km_cost"], 2)
    return 0.0

def compute_all_routes_and_scores(distance_km: float, road_travel_time_min: float) -> List[Dict]:
    """
    Computes duration, emissions, cost, and multi-criteria recommendation scores
    across all 4 modes (Metro, Public Bus, Electric Vehicle, ICE Private Car).
    """
    safe_duration_hours = max(road_travel_time_min / 60.0, 0.05)
    car_speed = max(min(distance_km / safe_duration_hours, 80.0), 5.0)

    modes = ["Metro", "Bus", "EV", "ICE_Car"]
    route_metrics = []

    for mode in modes:
        duration = calculate_mode_duration(mode, distance_km, road_travel_time_min)
        speed = car_speed if mode in ["ICE_Car", "EV"] else MODAL_PARAMS[mode]["speed_kmh"]
        
        emission_factor = calculate_arai_emission_factor(mode, speed)
        co2_kg = round((distance_km * emission_factor) / 1000.0, 2)
        cost = calculate_mode_cost(mode, distance_km)

        route_metrics.append({
            "mode": mode,
            "duration_min": round(duration, 1),
            "co2_emissions_kg": co2_kg,
            "estimated_cost_inr": cost
        })

    # Multi-Criteria Recommendation Scoring (MCDA)
    # Weights: 45% Carbon reduction, 35% Time efficiency, 20% Cost economy
    w_co2 = 0.45
    w_time = 0.35
    w_cost = 0.20

    min_co2 = min(r["co2_emissions_kg"] for r in route_metrics)
    max_co2 = max(r["co2_emissions_kg"] for r in route_metrics)
    min_time = min(r["duration_min"] for r in route_metrics)
    max_time = max(r["duration_min"] for r in route_metrics)
    min_cost = min(r["estimated_cost_inr"] for r in route_metrics)
    max_cost = max(r["estimated_cost_inr"] for r in route_metrics)

    for r in route_metrics:
        co2_score = 100.0 if max_co2 == min_co2 else ((max_co2 - r["co2_emissions_kg"]) / (max_co2 - min_co2)) * 100.0
        time_score = 100.0 if max_time == min_time else ((max_time - r["duration_min"]) / (max_time - min_time)) * 100.0
        cost_score = 100.0 if max_cost == min_cost else ((max_cost - r["estimated_cost_inr"]) / (max_cost - min_cost)) * 100.0

        raw_score = (w_co2 * co2_score) + (w_time * time_score) + (w_cost * cost_score)
        final_score = round(50.0 + (raw_score * 0.46), 1)
        r["recommendation_score"] = final_score

    route_metrics.sort(key=lambda x: x["recommendation_score"], reverse=True)
    return route_metrics


def calculate_profiled_emission_factor(
    profile_id: str,
    speed_kmh: float = 25.0,
    distance_km: float = 10.0,
    grid_region: str = "india_cea_national",
    occupancy_passengers: int = 40,
    occupancy_ratio: float = 1.0,
    rainfall_mm: float = 0.0,
    temperature_c: float = 25.0,
    cold_start: bool = False
) -> Dict[str, Any]:
    """
    Computes granular ARAI BS-VI / CEA emission factors across specific vehicle sub-classes,
    accounting for grid carbon intensity, passenger load factor, regenerative braking,
    cold-start warm-up penalties, and ambient weather adjustments.
    """
    if profile_id not in ARAI_VEHICLE_PROFILES:
        raise ValueError(f"Unsupported vehicle profile: {profile_id}")
    if grid_region not in GRID_CARBON_INTENSITY:
        raise ValueError(f"Unsupported grid region: {grid_region}")

    profile = ARAI_VEHICLE_PROFILES[profile_id]
    mode = profile["mode"]
    effective_speed = max(speed_kmh, 5.0)
    safe_dist = max(distance_km, 0.5)
    grid_kg_per_kwh = GRID_CARBON_INTENSITY[grid_region]

    notes: List[str] = []

    if mode == "ICE_Car":
        base_ef = profile["alpha"] + (profile["beta"] / effective_speed) + (profile["gamma"] * (effective_speed ** 2))
        if cold_start and profile.get("supports_cold_start", False) and safe_dist <= 5.0:
            cold_mult = 1.18 - (0.02 * safe_dist)
            base_ef *= max(cold_mult, 1.05)
            notes.append("Applied cold-start catalytic warm-up penalty for short urban trip.")
    elif mode == "EV" or profile_id == "ev_auto":
        # Stop-and-go urban speeds (<25 km/h) benefit slightly from regenerative braking recovery
        regen_factor = 0.92 if effective_speed < 25.0 else 1.0
        if regen_factor < 1.0:
            notes.append("Applied 8% urban regenerative braking efficiency gain.")
        base_ef = profile["kwh_per_km"] * grid_kg_per_kwh * 1000.0 * regen_factor
    elif mode == "Bus":
        passengers = max(occupancy_passengers, 1)
        if "kwh_per_km" in profile:
            fleet_g_km = profile["kwh_per_km"] * grid_kg_per_kwh * 1000.0
            notes.append(f"Electric bus grid intensity evaluated using {grid_region}.")
        else:
            fleet_g_km = profile["fleet_g_km"]
        base_ef = fleet_g_km / passengers
        notes.append(f"Per-passenger emissions normalized across {passengers} bus riders.")
    elif mode == "Metro":
        safe_occ = max(min(occupancy_ratio, 2.0), 0.25)
        grid_scale = grid_kg_per_kwh / GRID_CARBON_INTENSITY["india_cea_national"]
        base_ef = (profile["base_per_passenger_g_km"] * grid_scale) / safe_occ
        notes.append(f"Metro per-passenger intensity scaled for {grid_region} and {safe_occ}x load.")
    else:
        base_ef = profile["fixed_factor"]

    # Weather friction & HVAC adjustments consistent with calculate_weather_adjusted_emission_factor
    rain_penalty = 0.0
    if rainfall_mm > 0.0:
        if mode == "ICE_Car":
            rain_penalty = min(rainfall_mm * 0.015, 0.18)
        elif mode in ("EV", "Auto"):
            rain_penalty = min(rainfall_mm * 0.012, 0.15)
        elif mode == "Bus":
            rain_penalty = min(rainfall_mm * 0.008, 0.10)

    temp_penalty = 0.0
    if temperature_c > 32.0 and mode in ("ICE_Car", "EV"):
        temp_penalty = min((temperature_c - 32.0) * 0.01, 0.10)

    adjusted_ef = round(base_ef * (1.0 + rain_penalty + temp_penalty), 2)
    total_co2_kg = round((safe_dist * adjusted_ef) / 1000.0, 3)

    return {
        "profile_id": profile_id,
        "label": profile["label"],
        "mode": mode,
        "grid_region": grid_region,
        "distance_km": round(safe_dist, 2),
        "speed_kmh": round(effective_speed, 1),
        "base_emission_factor_g_km": round(base_ef, 2),
        "weather_adjusted_emission_factor_g_km": adjusted_ef,
        "total_co2_kg": total_co2_kg,
        "ecological_offset_vs_sedan": calculate_carbon_offset_impact(
            max(((safe_dist * calculate_arai_emission_factor("ICE_Car", effective_speed)) / 1000.0) - total_co2_kg, 0.0)
        ),
        "modeling_notes": notes
    }
