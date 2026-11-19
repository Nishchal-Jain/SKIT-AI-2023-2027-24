
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
import { MapPin, Navigation, LoaderCircle, AlertCircle } from 'lucide-react';

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

      const coordinatesAreValid = [
        ...originPosition,
        ...destinationPosition,
      ].every(Number.isFinite);

      if (!coordinatesAreValid) {
        setLoadingRoute(false);
        setRouteError(
          'The selected locations have invalid coordinates.'
        );
        return;
      }

      setLoadingRoute(true);

      try {
        const start = `${originPosition[1]},${originPosition[0]}`;
        const end = `${destinationPosition[1]},${destinationPosition[0]}`;

        const url =
          `https://router.project-osrm.org/route/v1/driving/` +
          `${start};${end}?overview=full&geometries=geojson`;

        const response = await fetch(url);

        if (!response.ok) {
          throw new Error(
            `Routing service returned ${response.status}.`
          );
        }

        const data = await response.json();

        if (
          data.code !== 'Ok' ||
          !data.routes?.[0]?.geometry?.coordinates
        ) {
          throw new Error(
            'No drivable route was found between these locations.'
          );
        }

        const positions = data.routes[0].geometry.coordinates.map(
          ([lng, lat]) => [lat, lng]
        );

        if (!cancelled) {
          setRouteCoordinates(positions);
        }
      } catch (error) {
        if (!cancelled) {
          setRouteError(
            error.message ||
            'Unable to load the road route. Please try again.'
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
    <div className="map-view-shell">

      <div className="map-top-overlay">
        <div className="map-route-label">
          <div className="map-route-icon">
            <Navigation size={17} />
          </div>

          <div>
            <strong>Live Route View</strong>
            <span>
              {origin && destination
                ? 'Selected journey'
                : 'Explore the city map'}
            </span>
          </div>
        </div>

        <span className="map-provider-badge">
          <MapPin size={13} />
          OpenStreetMap
        </span>
      </div>

      <MapContainer
        center={DEFAULT_CENTER}
        zoom={12}
        scrollWheelZoom={true}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {originPosition && (
          <Marker position={originPosition}>
            <Popup>
              Origin: {origin.name || 'Selected starting point'}
            </Popup>
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
            pathOptions={{
              color: '#07845d',
              weight: 6,
              opacity: 0.9,
              lineCap: 'round',
              lineJoin: 'round',
            }}
          />
        )}

        <RouteBounds positions={boundsPositions} />
      </MapContainer>

      {loadingRoute && (
        <div className="map-message map-loading" role="status">
          <LoaderCircle size={17} className="map-spinner" />
          Loading road route...
        </div>
      )}

      {routeError && (
        <div className="map-message map-error" role="alert">
          <AlertCircle size={17} />
          {routeError}
        </div>
      )}

      {!origin && !destination && (
        <div className="map-empty-hint">
          <div className="map-empty-icon">
            <MapPin size={23} />
          </div>
          <strong>Ready to explore?</strong>
          <span>Enter your starting point and destination to view your route.</span>
        </div>
      )}

      {origin && destination && !loadingRoute && !routeError &&
        routeCoordinates.length > 0 && (
          <div className="map-success-indicator">
            <span></span>
            Route displayed
          </div>
        )}
    </div>
  );
}
