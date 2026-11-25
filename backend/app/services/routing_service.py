import os
from typing import Any, Dict, List

import requests

from app.services.emission_calculator import (
    MODAL_PARAMS,
    calculate_arai_emission_factor,
    calculate_carbon_offset_impact,
    calculate_mode_cost,
    calculate_profiled_emission_factor,
    haversine_distance_km,
)
from app.services.gtfs_parser import find_nearest_transit_stops

OSRM_BASE_URL = os.getenv("OSRM_BASE_URL", "http://router.project-osrm.org")
URBAN_CIRCUITY_FACTOR = 1.28  # Bengaluru road network detour ratio vs straight-line distance
WALK_THRESHOLD_KM = 0.80      # Beyond 800m, commuters typically shift from walking to feeder/auto
WALK_SPEED_KMH = 4.8
FEEDER_AUTO_SPEED_KMH = 18.0


def get_road_distance_km(
    origin_lat: float,
    origin_lon: float,
    dest_lat: float,
    dest_lon: float,
    use_external_osrm: bool = False
) -> Dict[str, Any]:
    """
    Computes road distance (km) via OSRM when enabled, with automatic NFR-002
    fallback to Haversine distance adjusted by Bengaluru urban road circuity (1.28x).
    """
    straight_km = haversine_distance_km(origin_lat, origin_lon, dest_lat, dest_lon)
    fallback_road_km = round(max(straight_km * URBAN_CIRCUITY_FACTOR, 0.5), 2)

    if use_external_osrm:
        url = (
            f"{OSRM_BASE_URL}/route/v1/driving/"
            f"{origin_lon},{origin_lat};{dest_lon},{dest_lat}?overview=false"
        )
        try:
            resp = requests.get(url, timeout=2.0)
            resp.raise_for_status()
            routes = resp.json().get("routes", [])
            if routes:
                osrm_km = round(max(routes[0]["distance"] / 1000.0, 0.5), 2)
                return {"road_distance_km": osrm_km, "source": "osrm"}
        except requests.RequestException:
            pass

    return {"road_distance_km": fallback_road_km, "source": "haversine_circuity_fallback"}


def _compute_access_leg_metrics(distance_km: float, preferred_access_mode: str) -> Dict[str, Any]:
    """Computes emissions, time, and cost for a first-mile or last-mile feeder leg."""
    if distance_km <= 0.05:
        return {"mode": "walk", "distance_km": 0.0, "co2_kg": 0.0, "duration_min": 0.0, "cost_inr": 0.0}

    effective_mode = "walk" if (preferred_access_mode == "auto" and distance_km <= WALK_THRESHOLD_KM) else preferred_access_mode
    if preferred_access_mode == "auto" and distance_km > WALK_THRESHOLD_KM:
        effective_mode = "auto_rickshaw_cng"

    if effective_mode == "walk":
        return {
            "mode": "walk",
            "distance_km": round(distance_km, 2),
            "co2_kg": 0.0,
            "duration_min": round((distance_km / WALK_SPEED_KMH) * 60.0, 1),
            "cost_inr": 0.0,
        }

    if effective_mode == "feeder_bus":
        ef_g_km = calculate_arai_emission_factor("Bus", 16.0)
        co2_kg = round((distance_km * ef_g_km) / 1000.0, 3)
        return {
            "mode": "feeder_bus",
            "distance_km": round(distance_km, 2),
            "co2_kg": co2_kg,
            "duration_min": round((distance_km / 16.0) * 60.0 + 2.0, 1),
            "cost_inr": round(max(5.0, distance_km * 2.0), 2),
        }

    # CNG Auto or EV Auto feeder
    profile = "ev_auto" if effective_mode == "ev_auto" else "auto_rickshaw_cng"
    res = calculate_profiled_emission_factor(
        profile_id=profile,
        speed_kmh=FEEDER_AUTO_SPEED_KMH,
        distance_km=distance_km,
    )
    fare = round(max(30.0, 30.0 + max(distance_km - 2.0, 0.0) * 15.0), 2)
    return {
        "mode": profile,
        "distance_km": round(distance_km, 2),
        "co2_kg": res["total_co2_kg"],
        "duration_min": round((distance_km / FEEDER_AUTO_SPEED_KMH) * 60.0 + 2.0, 1),
        "cost_inr": fare,
    }


def calculate_door_to_door_multimodal_emissions(
    origin_lat: float,
    origin_lon: float,
    dest_lat: float,
    dest_lon: float,
    car_speed_kmh: float = 22.0,
    preferred_access_mode: str = "auto",
    car_profile: str = "petrol_small",
    ev_profile: str = "ev_hatchback",
    grid_region: str = "india_cea_national"
) -> Dict[str, Any]:
    """
    Calculates true door-to-door emissions across Metro, Bus, EV, and ICE Car by combining:
    - Real GTFS spatial snapping (first-mile and last-mile distances via cKDTree)
    - Access feeder emissions (walking / CNG auto / EV auto / feeder bus)
    - ARAI BS-VI / CEA grid-adjusted trunk emissions
    """
    origin_stops = find_nearest_transit_stops(origin_lat, origin_lon)
    dest_stops = find_nearest_transit_stops(dest_lat, dest_lon)

    road_info = get_road_distance_km(origin_lat, origin_lon, dest_lat, dest_lon)
    direct_road_km = road_info["road_distance_km"]

    # 1. Metro Door-to-Door (First-mile -> BMRCL Metro -> Last-mile)
    o_metro = origin_stops["nearest_metro_station"]
    d_metro = dest_stops["nearest_metro_station"]
    metro_first_mile = _compute_access_leg_metrics(o_metro["access_distance_km"], preferred_access_mode)
    metro_last_mile = _compute_access_leg_metrics(d_metro["access_distance_km"], preferred_access_mode)
    metro_trunk_km = max(
        haversine_distance_km(o_metro["lat"], o_metro["lon"], d_metro["lat"], d_metro["lon"]) * 1.12,
        1.0,
    )
    metro_trunk = calculate_profiled_emission_factor(
        profile_id="bmrcl_metro",
        speed_kmh=MODAL_PARAMS["Metro"]["speed_kmh"],
        distance_km=metro_trunk_km,
        grid_region=grid_region,
    )
    metro_total_co2 = round(metro_first_mile["co2_kg"] + metro_trunk["total_co2_kg"] + metro_last_mile["co2_kg"], 3)
    metro_total_min = round(
        metro_first_mile["duration_min"]
        + (metro_trunk_km / MODAL_PARAMS["Metro"]["speed_kmh"]) * 60.0
        + MODAL_PARAMS["Metro"]["access_wait_min"]
        + metro_last_mile["duration_min"],
        1,
    )
    metro_total_cost = round(
        metro_first_mile["cost_inr"] + calculate_mode_cost("Metro", metro_trunk_km) + metro_last_mile["cost_inr"],
        2,
    )

    # 2. Bus Door-to-Door (First-mile -> BMTC Bus -> Last-mile)
    o_bus = origin_stops["nearest_bus_stop"]
    d_bus = dest_stops["nearest_bus_stop"]
    bus_first_mile = _compute_access_leg_metrics(o_bus["access_distance_km"], preferred_access_mode)
    bus_last_mile = _compute_access_leg_metrics(d_bus["access_distance_km"], preferred_access_mode)
    bus_trunk_km = max(
        haversine_distance_km(o_bus["lat"], o_bus["lon"], d_bus["lat"], d_bus["lon"]) * URBAN_CIRCUITY_FACTOR,
        1.0,
    )
    bus_trunk = calculate_profiled_emission_factor(
        profile_id="bmtc_non_ac",
        speed_kmh=MODAL_PARAMS["Bus"]["speed_kmh"],
        distance_km=bus_trunk_km,
        grid_region=grid_region,
    )
    bus_total_co2 = round(bus_first_mile["co2_kg"] + bus_trunk["total_co2_kg"] + bus_last_mile["co2_kg"], 3)
    bus_total_min = round(
        bus_first_mile["duration_min"]
        + (bus_trunk_km / MODAL_PARAMS["Bus"]["speed_kmh"]) * 60.0
        + MODAL_PARAMS["Bus"]["access_wait_min"]
        + bus_last_mile["duration_min"],
        1,
    )
    bus_total_cost = round(
        bus_first_mile["cost_inr"] + calculate_mode_cost("Bus", bus_trunk_km) + bus_last_mile["cost_inr"],
        2,
    )

    # 3. Direct EV & Direct ICE Private Car
    ev_trip = calculate_profiled_emission_factor(
        profile_id=ev_profile,
        speed_kmh=car_speed_kmh,
        distance_km=direct_road_km,
        grid_region=grid_region,
    )
    car_trip = calculate_profiled_emission_factor(
        profile_id=car_profile,
        speed_kmh=car_speed_kmh,
        distance_km=direct_road_km,
        grid_region=grid_region,
        cold_start=direct_road_km <= 5.0,
    )

    car_co2 = car_trip["total_co2_kg"]
    road_min = round((direct_road_km / max(car_speed_kmh, 5.0)) * 60.0, 1)

    options: List[Dict[str, Any]] = [
        {
            "mode": "Metro",
            "trunk_distance_km": round(metro_trunk_km, 2),
            "first_mile": metro_first_mile,
            "last_mile": metro_last_mile,
            "total_door_to_door_co2_kg": metro_total_co2,
            "total_duration_min": metro_total_min,
            "total_cost_inr": metro_total_cost,
            "co2_saved_vs_car_kg": round(max(car_co2 - metro_total_co2, 0.0), 3),
            "ecological_offset": calculate_carbon_offset_impact(max(car_co2 - metro_total_co2, 0.0)),
        },
        {
            "mode": "Bus",
            "trunk_distance_km": round(bus_trunk_km, 2),
            "first_mile": bus_first_mile,
            "last_mile": bus_last_mile,
            "total_door_to_door_co2_kg": bus_total_co2,
            "total_duration_min": bus_total_min,
            "total_cost_inr": bus_total_cost,
            "co2_saved_vs_car_kg": round(max(car_co2 - bus_total_co2, 0.0), 3),
            "ecological_offset": calculate_carbon_offset_impact(max(car_co2 - bus_total_co2, 0.0)),
        },
        {
            "mode": "EV",
            "trunk_distance_km": direct_road_km,
            "first_mile": None,
            "last_mile": None,
            "total_door_to_door_co2_kg": ev_trip["total_co2_kg"],
            "total_duration_min": road_min,
            "total_cost_inr": calculate_mode_cost("EV", direct_road_km),
            "co2_saved_vs_car_kg": round(max(car_co2 - ev_trip["total_co2_kg"], 0.0), 3),
            "ecological_offset": calculate_carbon_offset_impact(max(car_co2 - ev_trip["total_co2_kg"], 0.0)),
        },
        {
            "mode": "ICE_Car",
            "trunk_distance_km": direct_road_km,
            "first_mile": None,
            "last_mile": None,
            "total_door_to_door_co2_kg": car_co2,
            "total_duration_min": road_min,
            "total_cost_inr": calculate_mode_cost("ICE_Car", direct_road_km),
            "co2_saved_vs_car_kg": 0.0,
            "ecological_offset": calculate_carbon_offset_impact(0.0),
        },
    ]

    return {
        "direct_road_distance_km": direct_road_km,
        "distance_source": road_info["source"],
        "origin_snapped_stops": {
            "metro_station": o_metro["stop_name"],
            "metro_access_km": o_metro["access_distance_km"],
            "bus_stop": o_bus["stop_name"],
            "bus_access_km": o_bus["access_distance_km"],
        },
        "destination_snapped_stops": {
            "metro_station": d_metro["stop_name"],
            "metro_access_km": d_metro["access_distance_km"],
            "bus_stop": d_bus["stop_name"],
            "bus_access_km": d_bus["access_distance_km"],
        },
        "door_to_door_comparison": options,
    }
