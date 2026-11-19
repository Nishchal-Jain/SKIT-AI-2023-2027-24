# 🌿 Smart Sustainable Transport Optimization System — Frontend

## 📌 Overview

The **AI-Based Smart Sustainable Transport Optimization System** is a web application designed to support sustainable urban mobility through route planning, multimodal transportation comparisons, and explainable AI visualizations.

The frontend is developed using **React and Vite**. It provides an interactive interface where users can enter source and destination locations, view a map, request route recommendations, compare transportation alternatives, and explore factors that may influence predicted travel time.

The system aims to help users make more informed transportation decisions by considering travel duration, estimated cost, and carbon emissions.

**Current development status — 29 October 2026:** The frontend components, location autocomplete, routing form, interactive map, transportation comparison interface, and SHAP visualization component are present in the application. The frontend has been updated, synchronized with the latest `main` branch, and verified with a successful Vite production build. Complete integration of route-specific predictions, live traffic and weather data, and dynamic SHAP explanations remains in development.

## ✨ Features

### 1. Location Autocomplete

The routing form provides location search and selection functionality.

- Suggest locations as the user types.
- Search using OpenStreetMap Nominatim.
- Use Photon as a fallback location search service.
- Display matching locations in a dropdown.
- Store selected latitude and longitude coordinates.
- Use Fuse.js to rank close text matches among returned results.
- Validate that both source and destination locations have been selected before submitting a route request.

Fuzzy matching improves the ranking of similar location names but does not guarantee correction of every spelling mistake.

### 2. Route Planning Form

The routing form allows users to select a source and destination and request a route recommendation.

Key functionality includes:

- Source and destination selection.
- Validation of selected locations.
- Validation that the source and destination differ.
- Loading indicators during route requests.
- Error handling for unsuccessful requests.
- Submission of selected coordinates and the intended departure time to the backend.
- Display of the returned route result.

The form uses the Fetch API to communicate with the backend route-recommendation endpoint.

### 3. Interactive Map

The map component is implemented using **React Leaflet and Leaflet**, with OpenStreetMap providing the map tiles.

The map interface provides a geographic view for the transport planning application and serves as the visualization layer for route-related information.

The map component has been updated as part of the latest frontend development work. Complete route visualization depends on the availability and format of route data returned by the backend.

### 4. Multimodal Transportation Comparison

The comparison interface presents four transportation alternatives:

- Metro Rail
- Public Bus
- Electric Vehicle (EV)
- Internal Combustion Engine (ICE) Car

The interface is intended to compare transportation alternatives using:

- Estimated travel duration.
- Estimated travel cost.
- Estimated carbon dioxide emissions.

**Current limitation:** Demonstration values are not equivalent to live, route-specific predictions. Complete integration with backend calculations is still required for reliable dynamic comparisons.

### 5. Explainable AI (SHAP)

The SHAP visualization component is designed to explain factors influencing travel-time predictions.

The visualization includes factors such as:

- Base travel time.
- Peak-hour traffic impact.
- Rainfall and weather impact.

The component provides an interface for presenting prediction explanations. The current demonstration values should not be interpreted as genuine SHAP output from a live machine learning prediction.

Future integration will connect the visualization to actual model predictions and their corresponding feature contributions.

### 6. Responsive User Interface

The application uses reusable React components and CSS styling to organize the user interface.

The main dashboard brings together:

- Header and application branding.
- Route planning form.
- Interactive map.
- Transportation comparison interface.
- SHAP visualization.

The frontend is structured to support future improvements in accessibility, responsiveness, usability, and backend integration.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| React | Component-based UI development |
| JavaScript and JSX | Frontend logic and component structure |
| Vite | Development server and production build |
| CSS | Layout and styling |
| Tailwind CSS | Utility-based styling where configured |
| React Leaflet | React integration for interactive maps |
| Leaflet | Map rendering and interactions |
| OpenStreetMap | Map tiles and geographic data |
| Nominatim | Primary location search |
| Photon | Fallback location search |
| Fuse.js | Fuzzy matching and ranking of location suggestions |
| Fetch API | HTTP communication with external services and the backend |
| FastAPI | Backend API framework |

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

Install:

- Node.js
- npm
- Git (for version control and collaboration)

Verify the installations:

```bash
node -v
npm -v
git --version
```

## 🚀 Installation and Setup

### Step 1: Open the frontend directory

From the repository root:

```bash
cd frontend
```

### Step 2: Install dependencies

```bash
npm install
```

Fuse.js is already listed in the project's dependencies. If it is missing from your local installation or dependency configuration, install it with:

```bash
npm install fuse.js
```

### Step 3: Start the development server

```bash
npm run dev
```

Vite displays the local development URL, usually:

```text
http://localhost:5173/
```

Open the displayed URL in your browser.

### Step 4: Build for production

```bash
npm run build
```

### Step 5: Preview the production build

```bash
npm run preview
```

## 🔌 Backend Integration

The routing form sends requests to the backend route-recommendation endpoint:

```text
POST http://localhost:8000/api/v1/recommend-route
```

The request uses the following structure:

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
  "intended_departure": "2026-10-29T12:00:00.000Z"
}
```

The coordinates and timestamp above are examples. The application submits the coordinates selected by the user and the current departure timestamp.

**Important:** Verify that the running backend accepts this request schema and that its response matches the format expected by the frontend. The example does not establish that the endpoint is currently returning production-ready route predictions.

To run the frontend independently, start Vite without the Python backend. However, operations requiring backend responses will not work fully unless the backend is running and accessible.

## 🗺️ Location Search and Autocomplete Workflow

The routing form uses two public geocoding services:

- **Nominatim:** Primary location search.
- **Photon:** Fallback location search.

Fuse.js ranks similar text matches among the locations returned by the geocoding services.

The workflow is:

1. The user types a location name.
2. The frontend waits briefly before searching.
3. The geocoding service returns matching locations.
4. Fuse.js ranks close text matches.
5. The user selects a suggestion.
6. The frontend stores the selected coordinates.
7. The coordinates are submitted when the user requests a route.

Public geocoding services have usage policies and rate limits. Production deployments should follow the relevant service policies and consider caching, request throttling, and suitable error handling.

## 🧪 Testing and Validation

### Verified on 29 October 2026

- The frontend production build completed successfully using `npm run build`.
- Vite transformed 1,947 modules.
- The generated production assets were written to the `dist/` directory.

Build command:

```bash
npm run build
```

### Recommended functional testing

- [ ] Frontend starts without errors.
- [ ] Dashboard and header render correctly.
- [ ] Source location autocomplete works.
- [ ] Destination location autocomplete works.
- [ ] Fallback geocoding works when needed.
- [ ] Fuzzy matching ranks similar location names.
- [ ] Both locations must be selected before submission.
- [ ] Identical source and destination coordinates are rejected.
- [ ] Selected coordinates are submitted correctly.
- [ ] Loading and backend error states display appropriately.
- [ ] Map visualization renders correctly.
- [ ] Route data is displayed correctly when returned by the backend.
- [ ] Transportation comparison cards render correctly.
- [ ] SHAP visualization renders correctly.
- [ ] `npm run build` completes successfully.
- [ ] `npm run lint` completes successfully.

The production build was verified. The remaining checklist items should be tested individually; successful compilation alone does not prove that every feature works end to end.

## 🚧 Current Limitations

- Fuzzy matching cannot guarantee correction of every misspelled location.
- Public geocoding services may be unavailable or rate-limited.
- Backend integration depends on matching request and response schemas.
- Complete live route calculations and route-specific predictions require further integration.
- Transportation comparison values are not yet fully connected to live route calculations.
- SHAP visualization values are not yet connected to genuine model explanations.
- Live traffic, weather, route-specific emissions, and cost estimates require validated backend integration.
- A successful production build does not establish the accuracy of machine learning predictions or emissions estimates.

## 🔮 Future Enhancements

- Improve spelling correction and location search ranking.
- Display calculated routes on the map.
- Connect route calculations to the transportation comparison interface.
- Integrate traffic and weather information.
- Validate transportation-specific emissions and cost calculations.
- Display actual machine learning predictions.
- Connect SHAP visualizations to genuine model output.
- Improve accessibility, responsiveness, and error handling.
- Add automated frontend tests.
- Improve API error handling, loading states, and integration testing.

## 🔄 GitHub Development Workflow

The frontend is maintained on the `frontend-dev` branch, while the shared integration branch is `main`.

The team's workflow is:

1. Fetch the latest repository changes.
2. Synchronize `frontend-dev` with `main` when required.
3. Implement and test frontend changes.
4. Commit and push changes to `frontend-dev`.
5. Create a Pull Request from `frontend-dev` into `main`.
6. Review and merge the Pull Request.
7. Synchronize `frontend-dev` with the updated `main` before continuing development.

### Frontend work completed on 29 October 2026

- Updated the frontend application and routing-related components.
- Synchronized the frontend branch with previously merged backend changes.
- Resolved and completed the Git merge workflow.
- Verified the Vite production build.
- Created and merged Pull Request #9, titled **feat(frontend): improve routing interface and map integration**.
- Synchronized `frontend-dev` with the updated `main` after the PR merge.
- Confirmed that `frontend-dev` and `main` were aligned on GitHub.

The latest branch status showed `frontend-dev` with zero commits ahead of or behind `main`. The `backend-dev` branch remains separate and is maintained through its own workflow.

## 🎯 Project Goal

To provide an intuitive interface for exploring transportation alternatives and supporting more sustainable urban mobility decisions through route information, transportation comparisons, and explainable AI.

---

**Project:** AI-Based Smart Sustainable Transport Optimization System  
**Frontend:** React + Vite  
**Mapping:** React Leaflet + OpenStreetMap  
**Geocoding:** Nominatim + Photon  
**Autocomplete Matching:** Fuse.js  
**Backend:** Python + FastAPI  
**Version Control:** Git + GitHub