from app.services.gtfs_parser import find_nearest_transit_stops, get_transit_index
from app.services.routing_service import (
    calculate_door_to_door_multimodal_emissions,
    get_road_distance_km,
)


def test_gtfs_spatial_index_loads_real_data_and_is_fast():
    index = get_transit_index()
    assert len(index.metro_stops) > 20
    assert len(index.bus_stops) > 100

    # Query near MG Road Bengaluru
    res = find_nearest_transit_stops(12.9756, 77.6066)
    assert res["nearest_metro_station"]["access_distance_km"] < 1.0
    assert res["nearest_bus_stop"]["access_distance_km"] < 1.0
    # Verify <20ms spatial snapping (typically <2ms after cache warmup)
    assert res["spatial_lookup_ms"] < 20.0


def test_road_distance_circuity_fallback():
    res = get_road_distance_km(12.9716, 77.5946, 12.9352, 77.6245, use_external_osrm=False)
    assert res["road_distance_km"] > 4.0
    assert res["source"] == "haversine_circuity_fallback"


def test_door_to_door_emissions_includes_first_and_last_mile():
    # Indiranagar to Koramangala
    res = calculate_door_to_door_multimodal_emissions(
        origin_lat=12.9784,
        origin_lon=77.6408,
        dest_lat=12.9279,
        dest_lon=77.6271,
        car_speed_kmh=20.0,
        preferred_access_mode="auto",
    )
    assert res["direct_road_distance_km"] > 4.0
    assert "origin_snapped_stops" in res
    assert "destination_snapped_stops" in res

    by_mode = {m["mode"]: m for m in res["door_to_door_comparison"]}
    assert by_mode["Metro"]["first_mile"] is not None
    assert by_mode["Metro"]["last_mile"] is not None
    # Even with first/last mile auto legs, Metro or Bus beats ICE Car CO2 significantly
    assert by_mode["Metro"]["total_door_to_door_co2_kg"] < by_mode["ICE_Car"]["total_door_to_door_co2_kg"]
    assert by_mode["Bus"]["total_door_to_door_co2_kg"] < by_mode["ICE_Car"]["total_door_to_door_co2_kg"]
