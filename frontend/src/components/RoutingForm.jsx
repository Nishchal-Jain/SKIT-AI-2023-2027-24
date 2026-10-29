
import React, { useEffect, useRef, useState } from 'react';
import Fuse from 'fuse.js';

const GEOCODING_URL = 'https://nominatim.openstreetmap.org/search';
const FALLBACK_GEOCODING_URL = 'https://photon.komoot.io/api/';
const API_URL = 'http://localhost:8000/api/v1/recommend-route';

const MIN_QUERY_LENGTH = 3;
const SEARCH_DELAY = 1000;

// Convert geocoding results into one consistent format.
function normalizePlace(place, provider) {
  if (provider === 'photon') {
    const p = place.properties || {};

    return {
      place_id: `photon-${p.osm_type}-${p.osm_id}`,
      display_name: [
        p.name,
        p.street,
        p.city || p.town || p.village,
        p.state,
        p.country,
      ]
        .filter(Boolean)
        .filter((value, index, array) => array.indexOf(value) === index)
        .join(', '),
      lat: Number(place.geometry.coordinates[1]),
      lon: Number(place.geometry.coordinates[0]),
    };
  }

  return {
    place_id: place.place_id,
    display_name: place.display_name,
    lat: Number(place.lat),
    lon: Number(place.lon),
  };
}

async function searchLocations(query, signal) {
  const params = new URLSearchParams({
    q: query,
    format: 'jsonv2',
    limit: '8',
    countrycodes: 'in',
    addressdetails: '1',
  });

  const response = await fetch(`${GEOCODING_URL}?${params}`, {
    signal,
  });

  if (!response.ok) {
    throw new Error('Location search failed.');
  }

  const data = await response.json();

  return data.map((place) => normalizePlace(place, 'nominatim'));
}

async function searchFallback(query, signal) {
  const params = new URLSearchParams({
    q: query,
    limit: '8',
    lang: 'en',
    lat: '12.9716',
    lon: '77.5946',
  });

  const response = await fetch(`${FALLBACK_GEOCODING_URL}?${params}`, {
    signal,
  });

  if (!response.ok) {
    throw new Error('Fallback location search failed.');
  }

  const data = await response.json();

  return (data.features || []).map((place) =>
    normalizePlace(place, 'photon')
  );
}

function rankLocations(places, query) {
  const uniquePlaces = Array.from(
    new Map(
      places
        .filter(
          (place) =>
            place.display_name &&
            Number.isFinite(place.lat) &&
            Number.isFinite(place.lon)
        )
        .map((place) => [
          `${place.lat},${place.lon}`,
          place,
        ])
    ).values()
  );

  const fuse = new Fuse(uniquePlaces, {
    keys: ['display_name'],
    threshold: 0.6,
    ignoreLocation: true,
    includeScore: true,
  });

  const matches = fuse.search(query);

  // Show close text matches first, followed by other geocoding results.
  return [
    ...matches.map((match) => match.item),
    ...uniquePlaces.filter(
      (place) =>
        !matches.some(
          (match) => match.item.place_id === place.place_id
        )
    ),
  ].slice(0, 8);
}

function LocationInput({
  label,
  value,
  onChange,
  selectedPlace,
  onSelect,
  placeholder,
}) {
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const [error, setError] = useState('');
  const [searchedQuery, setSearchedQuery] = useState('');

  const requestRef = useRef(0);

  useEffect(() => {
    const query = value.trim();

    if (selectedPlace || query.length < MIN_QUERY_LENGTH) {
      setSuggestions([]);
      setOpen(false);
      setError('');
      setSearchedQuery('');
      setLoading(false);
      return;
    }

    let cancelled = false;
    const controller = new AbortController();
    const requestId = ++requestRef.current;

    const timer = setTimeout(async () => {
      setLoading(true);
      setError('');
      setSearchedQuery(query);

      try {
        let places = [];

        // First try the OpenStreetMap geocoder.
        try {
          places = await searchLocations(query, controller.signal);
        } catch (err) {
          if (err.name === 'AbortError') throw err;
          // Try the fallback geocoder if the first service fails.
        }

        // If no results, or no close text matches, try Photon.
        const closeMatches =
          places.length > 0 ? rankLocations(places, query) : [];

        if (places.length === 0 || closeMatches.length === 0) {
          try {
            const fallbackPlaces = await searchFallback(
              query,
              controller.signal
            );

            places = [...places, ...fallbackPlaces];
          } catch (err) {
            if (err.name === 'AbortError') throw err;

            // Keep any results from the first provider.
            if (places.length === 0) throw err;
          }
        }

        if (!cancelled && requestId === requestRef.current) {
          setSuggestions(rankLocations(places, query));
          setOpen(true);
        }
      } catch (err) {
        if (
          !cancelled &&
          requestId === requestRef.current &&
          err.name !== 'AbortError'
        ) {
          setError('Location search failed. Please try again.');
          setSuggestions([]);
          setOpen(true);
        }
      } finally {
        if (!cancelled && requestId === requestRef.current) {
          setLoading(false);
        }
      }
    }, SEARCH_DELAY);

    return () => {
      cancelled = true;
      clearTimeout(timer);
      controller.abort();
    };
  }, [value, selectedPlace]);

  function handleChange(event) {
    onChange(event.target.value);
    onSelect(null);
    setError('');
    setOpen(false);
  }

  function choosePlace(place) {
    onChange(place.display_name);

    onSelect({
      name: place.display_name,
      lat: place.lat,
      lng: place.lon,
    });

    setSuggestions([]);
    setOpen(false);
    setError('');
  }

  return (
    <div className="relative">
      <label className="block text-xs font-medium text-slate-500 mb-1">
        {label}
      </label>

      <input
        type="text"
        value={value}
        onChange={handleChange}
        onFocus={() => {
          if (suggestions.length > 0) setOpen(true);
        }}
        onBlur={() => {
          setTimeout(() => setOpen(false), 150);
        }}
        placeholder={placeholder}
        autoComplete="off"
        required
        role="combobox"
        aria-expanded={open}
        aria-autocomplete="list"
        aria-controls={`${label.replace(/\s+/g, '-')}-suggestions`}
        className="w-full p-2.5 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 outline-none"
      />

      {loading && (
        <p className="text-xs text-slate-500 mt-1">
          Searching locations...
        </p>
      )}

      {error && (
        <p role="alert" className="text-xs text-red-600 mt-1">
          {error}
        </p>
      )}

      {open && suggestions.length > 0 && (
        <ul
          id={`${label.replace(/\s+/g, '-')}-suggestions`}
          role="listbox"
          className="absolute z-[1000] top-full left-0 right-0 mt-1 bg-white border border-slate-200 rounded-lg shadow-lg max-h-52 overflow-y-auto"
        >
          {suggestions.map((place) => (
            <li
              key={place.place_id}
              role="option"
              aria-selected="false"
            >
              <button
                type="button"
                onMouseDown={(event) => event.preventDefault()}
                onClick={() => choosePlace(place)}
                className="w-full text-left px-3 py-2.5 text-sm text-slate-700 hover:bg-emerald-50 border-b border-slate-100 last:border-0"
              >
                <span className="block font-medium">
                  {place.display_name.split(',')[0]}
                </span>

                <span className="block text-xs text-slate-500 mt-0.5">
                  {place.display_name}
                </span>
              </button>
            </li>
          ))}
        </ul>
      )}

      {open &&
        !loading &&
        !error &&
        searchedQuery.length >= MIN_QUERY_LENGTH &&
        suggestions.length === 0 && (
          <p className="text-xs text-slate-500 mt-1">
            No matching locations found. Try a nearby landmark or
            include the city name.
          </p>
        )}
    </div>
  );
}

export default function RoutingForm({ onRouteCalculated }) {
  const [origin, setOrigin] = useState('');
  const [destination, setDestination] = useState('');

  const [originPlace, setOriginPlace] = useState(null);
  const [destinationPlace, setDestinationPlace] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);

  async function handleSubmit(event) {
    event.preventDefault();
    setError('');
    setResult(null);

    if (!originPlace || !destinationPlace) {
      setError(
        'Select both source and destination from the location suggestions.'
      );
      return;
    }

    if (
      originPlace.lat === destinationPlace.lat &&
      originPlace.lng === destinationPlace.lng
    ) {
      setError('Source and destination must be different locations.');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          origin: {
            lat: originPlace.lat,
            lng: originPlace.lng,
          },
          destination: {
            lat: destinationPlace.lat,
            lng: destinationPlace.lng,
          },
          intended_departure: new Date().toISOString(),
        }),
      });

      if (!response.ok) {
        const message = await response.text();
        throw new Error(message || `Request failed: ${response.status}`);
      }

      const data = await response.json();

      setResult(data);

      if (onRouteCalculated) {
  onRouteCalculated({
    prediction: data,
    origin: originPlace,
    destination: destinationPlace,
  });
}
    } catch (err) {
      console.error('Route calculation failed:', err);

      setError(
        err.message ||
          'Could not calculate the route. Check that the backend is running.'
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
      <h2 className="text-lg font-semibold text-slate-800 mb-4">
        Plan Your Eco-Friendly Route
      </h2>

      <form className="space-y-4" onSubmit={handleSubmit}>
        <LocationInput
          label="Source Location"
          value={origin}
          onChange={setOrigin}
          selectedPlace={originPlace}
          onSelect={setOriginPlace}
          placeholder="e.g., Majestic, Bengaluru"
        />

        <LocationInput
          label="Destination Location"
          value={destination}
          onChange={setDestination}
          selectedPlace={destinationPlace}
          onSelect={setDestinationPlace}
          placeholder="e.g., Indiranagar, Bengaluru"
        />

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-emerald-600 hover:bg-emerald-700 disabled:opacity-60 text-white font-medium py-2.5 rounded-lg transition-colors text-sm"
        >
          {loading ? 'Calculating...' : 'Calculate Route & Emissions'}
        </button>

        {error && (
          <p role="alert" className="text-sm text-red-600 break-words">
            {error}
          </p>
        )}

        {result && (
          <div className="p-3 bg-emerald-50 rounded-lg text-sm text-slate-700">
            <p className="font-semibold text-emerald-800">
              Route response received
            </p>

            <pre className="mt-2 whitespace-pre-wrap break-words text-xs">
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        )}
      </form>

      <p className="text-[10px] text-slate-400 mt-4">
        Location data © OpenStreetMap contributors
      </p>
    </div>
  );
}
