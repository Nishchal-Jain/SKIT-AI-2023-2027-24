import csv
import re
import time
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
from scipy.spatial import cKDTree

from app.core.config import settings
from app.services.emission_calculator import haversine_distance_km

POINT_PATTERN = re.compile(r"POINT\s*\(\s*([-\d.]+)\s+([-\d.]+)\s*\)")

# NFR-002 fallback transit hubs if raw GTFS feeds are unavailable
FALLBACK_METRO_STOPS = [
    {"stop_id": "MG_RD", "stop_name": "Mahatma Gandhi Road", "lat": 12.9756, "lon": 77.6066},
    {"stop_id": "INDN", "stop_name": "Indiranagar", "lat": 12.9784, "lon": 77.6384},
    {"stop_id": "MAJ", "stop_name": "Nadaprabhu Kempegowda Station, Majestic", "lat": 12.9757, "lon": 77.5728},
    {"stop_id": "BYPH", "stop_name": "Baiyappanahalli", "lat": 12.9908, "lon": 77.6524},
]

FALLBACK_BUS_STOPS = [
    {"stop_id": "BMTC_MAJ", "stop_name": "Kempegowda Bus Station (Majestic)", "lat": 12.9776, "lon": 77.5713},
    {"stop_id": "BMTC_SHV", "stop_name": "Shivajinagara Bus Station", "lat": 12.9840, "lon": 77.6032},
    {"stop_id": "BMTC_KRM", "stop_name": "Koramangala Water Tank", "lat": 12.9304, "lon": 77.6245},
]


def _load_metro_stops(gtfs_dir: Path) -> List[Dict[str, Any]]:
    """Loads parent BMRCL Metro stations (location_type == '1') from GTFS stops.txt."""
    stops_file = gtfs_dir / "stops.txt"
    if not stops_file.exists():
        return FALLBACK_METRO_STOPS

    stations: List[Dict[str, Any]] = []
    seen_ids = set()
    with open(stops_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Prefer parent station nodes (location_type == '1') to avoid duplicate platforms/entrances
            if row.get("location_type", "").strip() not in ("1", ""):
                continue
            stop_id = (row.get("stop_id") or "").strip()
            if not stop_id or stop_id in seen_ids:
                continue
            try:
                lat = float(row["stop_lat"])
                lon = float(row["stop_lon"])
            except (KeyError, ValueError, TypeError):
                continue
            seen_ids.add(stop_id)
            stations.append({
                "stop_id": stop_id,
                "stop_name": (row.get("stop_name") or stop_id).strip(),
                "lat": lat,
                "lon": lon,
            })
    return stations or FALLBACK_METRO_STOPS


def _load_bmtc_bus_stops(gtfs_dir: Path) -> List[Dict[str, Any]]:
    """Loads BMTC Bus stop coordinates from GTFS stops.csv WKT POINT geometry."""
    stops_file = gtfs_dir / "stops.csv"
    if not stops_file.exists():
        return FALLBACK_BUS_STOPS

    stops: List[Dict[str, Any]] = []
    with open(stops_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            geom = (row.get("geometry") or "").strip()
            match = POINT_PATTERN.search(geom)
            if not match:
                continue
            try:
                lon = float(match.group(1))
                lat = float(match.group(2))
            except ValueError:
                continue
            stops.append({
                "stop_id": (row.get("id") or "").strip() or f"bmtc_{len(stops)}",
                "stop_name": (row.get("name") or "BMTC Stop").strip(),
                "lat": lat,
                "lon": lon,
            })
    return stops or FALLBACK_BUS_STOPS


class SpatialTransitIndex:
    """cKDTree spatial index enabling sub-2ms nearest Metro/Bus stop lookups."""

    def __init__(self, metro_stops: List[Dict[str, Any]], bus_stops: List[Dict[str, Any]]):
        self.metro_stops = metro_stops
        self.bus_stops = bus_stops
        self._metro_tree = cKDTree(np.array([[s["lat"], s["lon"]] for s in metro_stops]))
        self._bus_tree = cKDTree(np.array([[s["lat"], s["lon"]] for s in bus_stops]))

    def _query_nearest(
        self, tree: cKDTree, stops: List[Dict[str, Any]], lat: float, lon: float, k: int = 5
    ) -> Dict[str, Any]:
        top_k = min(k, len(stops))
        _, indices = tree.query([lat, lon], k=top_k)
        idx_list = [int(indices)] if top_k == 1 else [int(i) for i in indices]

        best_stop = None
        best_dist = float("inf")
        for idx in idx_list:
            candidate = stops[idx]
            dist_km = haversine_distance_km(lat, lon, candidate["lat"], candidate["lon"])
            if dist_km < best_dist:
                best_dist = dist_km
                best_stop = candidate

        return {
            **best_stop,
            "access_distance_km": round(best_dist, 2),
        }

    def nearest_metro(self, lat: float, lon: float) -> Dict[str, Any]:
        return self._query_nearest(self._metro_tree, self.metro_stops, lat, lon)

    def nearest_bus(self, lat: float, lon: float) -> Dict[str, Any]:
        return self._query_nearest(self._bus_tree, self.bus_stops, lat, lon)


@lru_cache(maxsize=1)
def get_transit_index() -> SpatialTransitIndex:
    """Loads and caches BMRCL Metro & BMTC Bus GTFS cKDTree indexes."""
    raw_dir = settings.BASE_DIR / "data" / "raw"
    metro_stops = _load_metro_stops(raw_dir / "gtfs_metro")
    bus_stops = _load_bmtc_bus_stops(raw_dir / "gtfs_bmtc")
    return SpatialTransitIndex(metro_stops=metro_stops, bus_stops=bus_stops)


def find_nearest_transit_stops(lat: float, lon: float) -> Dict[str, Any]:
    """Resolves nearest Namma Metro station and BMTC bus stop with lookup latency tracking."""
    index = get_transit_index()
    t0 = time.perf_counter()
    metro = index.nearest_metro(lat, lon)
    bus = index.nearest_bus(lat, lon)
    lookup_ms = round((time.perf_counter() - t0) * 1000.0, 3)

    return {
        "query_coordinates": {"lat": lat, "lng": lon},
        "nearest_metro_station": metro,
        "nearest_bus_stop": bus,
        "indexed_metro_stations": len(index.metro_stops),
        "indexed_bus_stops": len(index.bus_stops),
        "spatial_lookup_ms": lookup_ms,
    }
