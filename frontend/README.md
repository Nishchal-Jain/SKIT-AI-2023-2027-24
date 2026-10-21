# 🌿 Smart Sustainable Transport Optimization System — Frontend

## 📌 Overview

The frontend of the **AI-Based Smart Sustainable Transport Optimization System** is built with React and Vite. It provides an interactive interface for entering travel locations, viewing a map, comparing transportation modes, and displaying explainable AI visualizations.

The frontend is designed to support sustainable urban mobility by helping users explore travel time, estimated cost, and carbon emission comparisons.

**Development status:** The UI components and location autocomplete are implemented. Complete integration with real route calculations, machine learning predictions, weather data, and dynamic SHAP explanations is still under development.

## ✨ Features

### 1. Location Autocomplete

- Suggest locations as the user types.
- Search for locations using OpenStreetMap Nominatim.
- Use Photon as a fallback location search service.
- Display matching locations in a dropdown.
- Store the selected location's latitude and longitude.
- Use Fuse.js to rank close text matches among the locations returned by the geocoding services.
- Validate that both source and destination locations are selected before submitting the form.

**Note:** Fuzzy matching helps identify similar location names but does not guarantee correction of every spelling mistake.

### 2. Route Planning Form

The routing form allows users to enter:

- Source location
- Destination location

The form includes loading indicators, input validation, error messages, and a **Calculate Route & Emissions** button.

The selected coordinates are submitted to the backend route-recommendation endpoint.

### 3. Interactive Map

The map component uses:

- **Leaflet** for interactive map functionality
- **OpenStreetMap** for map tiles

The component provides map visualization and can be extended to display dynamically calculated routes.

### 4. Multimodal Transport Comparison

The comparison interface presents four transportation modes:

- Metro Rail
- Public Bus
- Electric Vehicle
- Internal Combustion Engine (ICE) Car

The UI displays estimated travel duration, CO₂ emissions, and travel cost.

The current comparison values are demonstration values and should not be treated as live route-specific predictions.

### 5. Explainable AI (SHAP)

The SHAP visualization component displays factors intended to explain travel-time predictions, including:

- Base travel time
- Peak-hour traffic impact
- Rainfall and weather impact

The current visualization uses demonstration values rather than dynamically generated SHAP output from a live model prediction.

### 6. Responsive User Interface

The frontend uses reusable React components and CSS styling to organize the route form, map, comparison cards, and explainability section.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| React | Component-based UI development |
| JavaScript (JSX) | Frontend application logic |
| Vite | Development server and build tool |
| CSS | Layout and styling |
| Leaflet | Interactive maps |
| OpenStreetMap | Map tiles and geographic data |
| Nominatim | Location search and geocoding |
| Photon | Fallback location search |
| Fuse.js | Fuzzy matching and ranking of location suggestions |
| Fetch API | HTTP requests to external services and the backend |

## 📂 Project Structure

```text
frontend/
├── public/
│   ├── favicon.svg
│   └── icons.svg
├── src/
│   ├── assets/
│   ├── components/
│   │   ├── Header.jsx
│   │   ├── MapView.jsx
│   │   ├── RoutingForm.jsx
│   │   ├── ModalComparison.jsx
│   │   └── ShapChart.jsx
│   ├── App.jsx
│   ├── App.css
│   ├── index.css
│   └── main.jsx
├── .gitignore
├── eslint.config.js
├── index.html
├── package.json
├── package-lock.json
├── vite.config.js
└── README.md
```

## ⚙️ Prerequisites

Install the following:

- Node.js
- npm
- Git (optional)

Verify the installations:

```bash
node -v
npm -v
```

## 🚀 Installation and Setup

### Step 1: Open the frontend directory

From the project root:

```bash
cd frontend
```

### Step 2: Install dependencies

```bash
npm install
```

Install Fuse.js if it is not already listed in the project dependencies:

```bash
npm install fuse.js
```

### Step 3: Start the development server

```bash
npm run dev
```

Vite will display a local development URL. It is usually:

```text
http://localhost:5173/
```

Open the displayed URL in your browser to view the frontend.

## 🔌 Backend Integration

The frontend sends route requests to:

```text
POST http://localhost:8000/api/v1/recommend-route
```

The current request format used by the routing form is:

```json
{
  "origin": {
    "lat": 12.9716,
    "lng": 77.5946
  },
  "destination": {
    "lat": 12.9352,
    "lng": 77.6245
  },
  "intended_departure": "2026-10-21T12:00:00.000Z"
}
```

The coordinates and departure time above are examples. The application submits the actual selected coordinates and current timestamp.

**Important:** Confirm that the backend accepts this exact request schema before testing the route endpoint. The current backend may return sample route results.

To view the frontend alone, you can start Vite without starting the Python backend. Features that require API responses will need the backend to be running.

## 🗺️ Location Search and Autocomplete

The routing form uses two public geocoding services:

- **Nominatim:** Primary location search.
- **Photon:** Fallback search when the primary service returns no results or fails.

Fuse.js ranks close text matches among the returned location results.

### Autocomplete workflow

1. The user types a location name.
2. The frontend waits briefly before searching.
3. The geocoding service returns matching locations.
4. The frontend ranks the returned locations.
5. The user selects a suggestion.
6. The selected coordinates are stored for route submission.

### Usage considerations

Public geocoding services have usage policies and rate limits. For production deployments, review the relevant service policies and consider routing requests through a backend service with suitable caching and rate limiting.

## 🏗️ Production Build

Create an optimized frontend build:

```bash
npm run build
```

The generated files are placed in the `dist/` directory.

Preview the production build locally:

```bash
npm run preview
```

## 🔍 Code Quality

Run the configured ESLint checks:

```bash
npm run lint
```

## 🧪 Testing Checklist

- [ ] Frontend starts without errors.
- [ ] Main dashboard renders correctly.
- [ ] Header and UI components display correctly.
- [ ] Source location autocomplete works.
- [ ] Destination location autocomplete works.
- [ ] Fallback location search works when needed.
- [ ] Fuzzy matching ranks similar location names.
- [ ] Users must select both locations before submission.
- [ ] Selected coordinates are submitted to the backend.
- [ ] Backend errors are displayed appropriately.
- [ ] Map visualization works.
- [ ] Transport comparison cards display correctly.
- [ ] SHAP visualization renders correctly.
- [ ] Production build completes successfully.

## 🚧 Current Limitations

- Fuzzy matching cannot guarantee correction of every misspelled location.
- Public geocoding services may be unavailable or rate-limited.
- The routing form depends on the backend request schema matching the submitted coordinates.
- The backend currently returns sample route results.
- Transport comparison cards are not yet fully connected to live route calculations.
- The SHAP visualization is not yet connected to actual model explanations.
- Real-time traffic, weather, route-specific emissions, and machine learning predictions require complete backend integration.

## 🔮 Future Enhancements

- Improve spelling correction and location search ranking.
- Display selected routes on the map.
- Connect live route calculations to transport comparisons.
- Integrate traffic and weather information.
- Calculate and validate transport-specific emissions and costs.
- Display actual machine learning predictions.
- Connect SHAP visualizations to genuine model output.
- Improve accessibility, responsiveness, and error handling.
- Add automated frontend tests.

## 🎯 Project Goal

To provide an intuitive interface for exploring transportation alternatives and supporting more sustainable urban mobility decisions through route information, transport comparisons, and explainable AI.

---

**Project:** AI-Based Smart Sustainable Transport Optimization System  
**Frontend:** React + Vite  
**Mapping:** Leaflet + OpenStreetMap  
**Geocoding:** Nominatim + Photon  
**Autocomplete Matching:** Fuse.js  
**Backend:** Python + FastAPI
