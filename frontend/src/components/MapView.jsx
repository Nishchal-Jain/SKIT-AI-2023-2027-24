import React, { useEffect, useState } from 'react';
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Polyline,
  useMap,
} from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const DEFAULT_CENTER = [12.9716, 77.5946];

function RouteBounds({ positions }) {
  const map = useMap();

  useEffect(() => {
    if (positions.length === 0) return;

    if (positions.length === 1) {
      map.setView(positions[0], 13);
      return;
    }

    map.fitBounds(L.latLngBounds(positions), {
      padding: [40, 40],
      maxZoom: 14,
    });
  }, [map, positions]);

  return null;
}

export default function MapView({ routeInfo }) {
  const [routeCoordinates, setRouteCoordinates] = useState([]);
  const [loadingRoute, setLoadingRoute] = useState(false);
  const [routeError, setRouteError] = useState('');

  const origin = routeInfo?.origin;
  const destination = routeInfo?.destination;

  const originPosition = origin
    ? [Number(origin.lat), Number(origin.lng)]
    : null;

  const destinationPosition = destination
    ? [Number(destination.lat), Number(destination.lng)]
    : null;

  useEffect(() => {
    let cancelled = false;

    async function fetchRoadRoute() {
      setRouteCoordinates([]);
      setRouteError('');

      if (!originPosition || !destinationPosition) {
        setLoadingRoute(false);
        return;
      }

      const coordinatesAreValid = [...originPosition, ...destinationPosition]
        .every(Number.isFinite);

      if (!coordinatesAreValid) {
        setLoadingRoute(false);
        setRouteError('The selected locations have invalid coordinates.');
        return;
      }

      setLoadingRoute(true);

      try {
        // OSRM uses longitude,latitude order.
        const start = `${originPosition[1]},${originPosition[0]}`;
        const end = `${destinationPosition[1]},${destinationPosition[0]}`;

        const url =
          `https://router.project-osrm.org/route/v1/driving/` +
          `${start};${end}?overview=full&geometries=geojson`;

        const response = await fetch(url);

        if (!response.ok) {
          throw new Error(`Routing service returned ${response.status}.`);
        }

        const data = await response.json();

        if (data.code !== 'Ok' || !data.routes?.[0]?.geometry?.coordinates) {
          throw new Error('No drivable route was found between these locations.');
        }

        // GeoJSON coordinates are [longitude, latitude].
        const positions = data.routes[0].geometry.coordinates.map(
          ([lng, lat]) => [lat, lng]
        );

        if (!cancelled) {
          setRouteCoordinates(positions);
        }
      } catch (error) {
        if (!cancelled) {
          setRouteError(
            error.message || 'Unable to load the road route. Please try again.'
          );
        }
      } finally {
        if (!cancelled) {
          setLoadingRoute(false);
        }
      }
    }

    fetchRoadRoute();

    return () => {
      cancelled = true;
    };
  }, [
    origin?.lat,
    origin?.lng,
    destination?.lat,
    destination?.lng,
  ]);

  const boundsPositions =
    routeCoordinates.length > 0
      ? routeCoordinates
      : [originPosition, destinationPosition].filter(Boolean);

  return (
    <div className="h-[500px] w-full rounded-xl overflow-hidden shadow-sm border border-slate-200 relative">
      <MapContainer
        center={DEFAULT_CENTER}
        zoom={12}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {originPosition && (
          <Marker position={originPosition}>
            <Popup>Origin: {origin.name || 'Selected starting point'}</Popup>
          </Marker>
        )}

        {destinationPosition && (
          <Marker position={destinationPosition}>
            <Popup>
              Destination: {destination.name || 'Selected destination'}
            </Popup>
          </Marker>
        )}

        {routeCoordinates.length > 0 && (
          <Polyline
            positions={routeCoordinates}
            pathOptions={{ color: '#16a34a', weight: 5, opacity: 0.85 }}
          />
        )}

        <RouteBounds positions={boundsPositions} />
      </MapContainer>

      {(loadingRoute || routeError) && (
        <div
          role="status"
          className="absolute top-3 left-3 z-[1000] max-w-sm rounded-lg bg-white px-3 py-2 text-sm shadow-md"
        >
          {loadingRoute && <p>Loading road route...</p>}
          {routeError && <p className="text-red-600">{routeError}</p>}
        </div>
      )}
    </div>
  );
}