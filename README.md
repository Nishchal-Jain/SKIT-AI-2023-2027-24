# 🌿 AI-Based Smart Sustainable Transport Optimization System
> **An AI-Powered Pre-Trip Decision Support System Integrating Real-Time Traffic Ingestion, Live Weather Telemetry, ARAI-Certified Multi-Modal Emission Benchmarking, and Explainable AI (SHAP) for Eco-Friendly Urban Transit.**

---

## 📜 Academic & Project Metadata

| Attribute | Details / Specification |
| :--- | :--- |
| **Institution** | Swami Keshvanand Institute of Technology, Management & Gramothan (SKIT), Jaipur |
| **Department** | Department of Computer Science & Engineering (Artificial Intelligence), Section B |
| **Academic Session** | 2026 – 2027 |
| **Project Track** | R&D Innovation Track (Target Evaluation: Research Paper Publication & Viva-Voce) |
| **UN SDG Alignment** | **SDG 11:** Sustainable Cities & Communities \| **SDG 13:** Climate Action |
| **Project Duration** | August 10, 2026 – March 6, 2027 (Five Sprints) |
| **Team Lead** | **Nishchal Jain** (Lead Backend, AI Models, MongoDB Atlas & Cloud Infrastructure) |
| **Team Member 1** | **Tanvi Sharma** (Lead Frontend, UI/UX Layouts, Leaflet Maps & Plotly Visualizations) |
| **Project Supervisor** | Department Faculty Mentor & SKIT Project Evaluation Committee |
| **Repository Type** | Full-Stack Monorepo (`backend/` + `frontend/`) |
| **Git Strategy** | Role-Based Development Branches (`backend-dev` & `frontend-dev`) with 1–2 Week Merge Cadence to `main` |

---

## 📑 Table of Contents
1. [Executive Summary & Problem Statement](#1-executive-summary--problem-statement)
2. [Core Innovation & System Architecture](#2-core-innovation--system-architecture)
3. [Technology Stack Specification Matrix](#3-technology-stack-specification-matrix)
4. [Complete Monorepo Directory Layout](#4-complete-monorepo-directory-layout)
5. [Detailed Developer Work Distribution & Form 2 Allocation](#5-detailed-developer-work-distribution--form-2-allocation)
6. [System Requirements Specification (FRs & NFRs)](#6-system-requirements-specification-frs--nfrs)
7. [Data Engineering & Ingestion Pipeline Specifications](#7-data-engineering--ingestion-pipeline-specifications)
8. [Machine Learning Architectures (XGBoost & Prophet)](#8-machine-learning-architectures-xgboost--prophet)
9. [ARAI Multi-Modal Emission Equations & Calculations](#9-arai-multi-modal-emission-equations--calculations)
10. [System Technical Deep Dive](#10-system-technical-deep-dive)
11. [Explainable AI (SHAP) Diagnostics](#11-explainable-ai-shap-diagnostics)
12. [API REST Gateway Specifications & OpenAPI Schemas](#12-api-rest-gateway-specifications--openapi-schemas)
13. [Frontend Architecture & React Component Tree](#13-frontend-architecture--react-component-tree)
14. [Automated Weekly Progress Report System (Form-3 PDF)](#14-automated-weekly-progress-report-system-form-3-pdf)
15. [Git Branching & 1–2 Week Merge Protocol](#15-git-branching--12-week-merge-protocol)
16. [Environment Variables & Security Configuration](#16-environment-variables--security-configuration)
17. [Step-by-Step Local Setup & Installation Guide](#17-step-by-step-local-setup--installation-guide)
18. [Developer Guidelines & Modular Interface Contracts](#18-developer-guidelines--modular-interface-contracts)
19. [Verification, Testing & Benchmarking Suite](#19-verification-testing--benchmarking-suite)
20. [Troubleshooting & Frequently Asked Questions](#20-troubleshooting--frequently-asked-questions)

---

## 1. 💡 Executive Summary & Problem Statement

### 1.1 The Urban Mobility Challenge
Modern navigation applications—such as Google Maps, Waze, and Apple Maps—are engineered around a single primary objective: **minimizing travel duration**. While effective for route selection based purely on time, this paradigm introduces severe ecological and operational drawbacks in urban environments:
* **Omission of Carbon Footprint:** Vehicle emissions ($CO_2$), particulate matter ($PM_{2.5}, PM_{10}$), and fuel consumption rates are completely excluded from routing algorithms.
* **Absence of Real-Time Multi-Modal Benchmarking:** Commuters are not provided with dynamic comparisons contrasting private Internal Combustion Engine (ICE) vehicles against Electric Vehicles (EVs), public buses, and electrified urban rail (Metro).
* **Uncoupled Weather-Traffic Dynamics:** Existing tools treat weather conditions (e.g., heavy monsoon downpours, extreme heat, reduced atmospheric visibility) as isolated alerts rather than factoring them into mathematical congestion and speed-loss models.
* **Black-Box Algorithmic Decision-Making:** Deep learning and spatiotemporal models fail to provide explainable feedback regarding *why* a particular route is congested or *why* an alternative transit mode is superior.

### 1.2 The Eco-Friendly Solution
The **AI-Based Smart Sustainable Transport Optimization System** serves as an intelligent **pre-trip decision support system**. Before a commuter departs, the platform ingests real-time spatial traffic data, live meteorological feeds, and vehicle physics parameters to calculate travel duration, monetary expenditure, and $CO_2$ footprint across four distinct modes of transport.

```
+-----------------------------------------------------------------------------------+
|                            PRE-TRIP USER COMMUTE INPUT                            |
|             Origin & Destination Coordinates | Intended Departure Time             |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                             LIVE TELEMETRY INGESTION                              |
|   +--------------------------+-----------------------+------------------------+   |
|   | Bangalore Traffic Pulse  | OpenWeather API Feed  | OSRM Map Distance API  |   |
|   +------------+-------------+-----------+-----------+-----------+------------+   |
+----------------|-------------------------|-----------------------|----------------+
                 |                         |                       |
                 v                         v                       v
+-----------------------------------------------------------------------------------+
|                            AI & EMISSION MODEL ENGINE                             |
|   +--------------------------+-----------------------+------------------------+   |
|   | XGBoost / LightGBM       | Facebook Prophet      | ARAI Multi-Modal       |   |
|   | Duration Predictor       | 2-Hr Traffic Trends   | Speed-Emission Factors |   |
|   +------------+-------------+-----------+-----------+-----------+------------+   |
+----------------|-------------------------|-----------------------|----------------+
                 |                         |                       |
                 v                         v                       v
+-----------------------------------------------------------------------------------+
|                        EXPLAINABLE AI (SHAP) EXPLAINER                            |
|           Quantifies delay factors: Rainfall % vs Peak Rush Hour %                |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                       REACT.JS DASHBOARD & DATA VISUALS                           |
|   +--------------------------+-----------------------+------------------------+   |
|   | Leaflet Traffic Maps     | Multi-Modal Transit   | Plotly SHAP Feature    |   |
|   | Color-Coded Polylines    | Comparison Cards      | Importance Breakdown   |   |
|   +--------------------------+-----------------------+------------------------+   |
+-----------------------------------------------------------------------------------+
```

---

## 2. 🌟 Core Innovation & System Architecture

### 2.1 Crucial Architectural Distinction
This platform is **explicitly designed as a pre-trip decision support system**, distinct from live turn-by-turn GPS navigation software. Its core purpose is to inform user modal selection (Metro vs. EV vs. Bus vs. ICE Car) *before* journey commencement.

| Architectural Dimension | Conventional Navigation (e.g. Google Maps) | Smart Sustainable Transport System |
| :--- | :--- | :--- |
| **Primary Objective** | Minimum Travel Duration | Multi-Objective Optimization (Time + $CO_2$ + Cost) |
| **Operational Phase** | Active In-Trip Guidance | Pre-Trip Decision Evaluation |
| **Environmental Awareness** | None ($0\%$ $CO_2$ visibility) | ARAI Speed-Dependent Emissions Benchmarking |
| **Explainability (XAI)** | Black-box routing | TreeSHAP feature attribution breakdown |
| **Traffic Horizon** | Instantaneous snapshots | Prophet 2-hour trend forecasting |
| **Public Transit Integration** | Basic timetable schedules | Live multi-modal carbon offset comparison |

---

## 3. 🛠️ Technology Stack Specification Matrix

| Component Layer | Technology / Library | Purpose & Specification |
| :--- | :--- | :--- |
| **Backend Framework** | Python 3.11+ / FastAPI | Asynchronous REST API server with Pydantic type enforcement |
| **ML Models** | XGBoost, LightGBM, Prophet | Travel time prediction & 2-hour traffic forecasting |
| **Explainable AI** | SHAP (SHapley Additive exPlanations) | Feature attribution quantifying delay drivers (rain, rush hour) |
| **Database** | MongoDB Atlas | Cloud NoSQL database storing user trips and audit logs |
| **Map Engine** | Leaflet.js, OpenStreetMap | Interactive spatial map rendering with color-coded traffic polylines |
| **Routing Engine** | OSRM (Open Source Routing Machine) | Distance matrix calculation and waypoint generation |
| **Frontend UI** | React.js (Vite), Tailwind CSS | Responsive dashboard with real-time modal comparison cards |
| **Visualizations** | Plotly.js, Chart.js | SHAP force plots, emission breakdown bar charts, traffic trends |
| **CI/CD & Reporting** | GitHub Actions, ReportLab | Automated weekly Form-3 progress PDF generation and commit tracking |

---

## 4. 📁 Complete Monorepo Directory Layout

```text
smart-sustainable-transport/
├── .github/
│   └── workflows/
│       └── auto_weekly_report.yml       # Automated Thursday Form-3 PDF generation
├── backend/                             # Python FastAPI & ML Engine (Nishchal Jain)
│   ├── app/
│   │   ├── api/
│   │   │   ├── endpoints.py             # REST API routes (/recommend-route, /predict-traffic)
│   │   │   └── router.py                # Router registry
│   │   ├── core/
│   │   │   ├── config.py                # Environment variables & MongoDB settings
│   │   │   └── database.py              # Async MongoDB Atlas connection manager
│   │   ├── models/
│   │   │   ├── xgboost_predictor.py     # XGBoost route travel time model
│   │   │   ├── prophet_forecaster.py    # Facebook Prophet 2-hour traffic trend model
│   │   │   └── shap_explainer.py        # TreeSHAP feature attribution explainer
│   │   ├── services/
│   │   │   ├── emission_calculator.py   # ARAI speed-dependent emission formulas
│   │   │   ├── weather_service.py       # OpenWeather API integration
│   │   │   ├── gtfs_parser.py           # GTFS data loader and shape extraction
│   │   │   └── routing_service.py       # OSRM distance matrix & spatial snapping
│   │   └── main.py                      # FastAPI app entry point & CORS configuration
│   ├── data/
│   │   ├── raw/
│   │   │   ├── bangalore_traffic_pulse.csv
│   │   │   ├── gtfs_metro/              # BMRCL Namma Metro (stops.txt, routes.txt, shapes.txt)
│   │   │   └── gtfs_bmtc/               # BMTC Bus (stops.txt, routes.txt, shapes.txt)
│   │   └── processed/                   # Feature-engineered training vectors
│   ├── tests/                           # PyTest test suite
│   ├── .env.example                     # Environment template for backend
│   └── requirements.txt                 # Python dependencies
├── frontend/                            # React.js & Tailwind CSS UI (Tanvi Sharma)
│   ├── src/
│   │   ├── components/
│   │   │   ├── MapView.jsx              # Leaflet map with colored polyline layers
│   │   │   ├── RoutingForm.jsx          # Source/Destination input with autocomplete
│   │   │   ├── ModalComparison.jsx      # Transit mode cards (Metro, EV, Bus, ICE)
│   │   │   └── ShapChart.jsx            # Plotly feature importance chart
│   │   ├── services/
│   │   │   └── api.js                   # Axios REST client for FastAPI endpoints
│   │   ├── App.jsx                      # Main dashboard layout
│   │   └── main.jsx                     # React DOM entry point
│   ├── package.json                     # Frontend dependencies
│   └── tailwind.config.js               # Tailwind styling configuration
├── weekly_reports/                      # Auto-generated Form-3 progress PDF archives
├── generate_report.py                   # Git commit parser & ReportLab PDF compiler
├── .gitignore                           # Repository build ignore definitions
└── README.md                            # System specification & engineering documentation
```

---

## 5. 👥 Detailed Developer Work Distribution & Form 2 Allocation

### 5.1 Nishchal Jain (Team Lead – Backend, AI & Cloud)
* **Sprint 1 (Aug 10 – Sep 18, 2026):** Ingestion & cleaning of Bangalore traffic dataset; OpenWeather API client setup; baseline XGBoost model setup.
* **Sprint 2 (Sep 19 – Oct 28, 2026):** Prophet model tuning for 2-hour traffic forecasting; ARAI emission calculation formulas implementation.
* **Sprint 3 (Oct 29 – Dec 08, 2026):** TreeSHAP explainability engine; FastAPI REST endpoints setup; MongoDB Atlas connection for trip logging.

### 5.2 Tanvi Sharma (Team Member 1 – Frontend, UI/UX & Maps)
* **Sprint 4 (Dec 09, 2026 – Jan 18, 2027):** Responsive dashboard layout in React.js & Tailwind CSS; Leaflet.js map integration with OSRM routing.
* **Sprint 5 (Jan 19 – Feb 25, 2027):** Plotly SHAP explanation charts; full API integration with FastAPI; final testing & submission prep.

---

## 6. 📋 System Requirements Specification (FRs & NFRs)

### Functional Requirements
* **FR-001 (Multi-Modal Routing):** System MUST accept origin/destination coordinates and calculate travel metrics across 4 modes: Metro, EV, Bus, ICE Car.
* **FR-002 (Real-Time Ingestion):** Ingest live weather data from OpenWeather API and spatial distance metrics from OSRM.
* **FR-003 (Emission Benchmarking):** Compute $CO_2$ emissions using ARAI speed-dependent curves.
* **FR-004 (2-Hour Traffic Forecasting):** Predict traffic congestion trends up to 2 hours ahead using Facebook Prophet.
* **FR-005 (Explainable AI Insights):** Provide TreeSHAP feature attributions detailing primary delay factors.
* **FR-006 (Trip Logging):** Save route searches and selected modes to MongoDB Atlas for sustainability analytics.

### Non-Functional Requirements
* **NFR-001 (API Performance):** End-to-end API response time MUST remain under 500ms (target average <200ms).
* **NFR-002 (System Reliability):** Fallback default values MUST be provided if third-party weather/routing APIs time out.
* **NFR-003 (Security):** All API credentials MUST be loaded from environment variables (`.env`).

---

## 7. 📊 Data Engineering & Ingestion Pipeline Specifications

### 7.1 Bangalore Traffic Pulse Dataset
Historical speed, travel duration, and congestion indices for XGBoost & Prophet models.

### 7.2 Namma Metro GTFS Static Feed (`gtfs_metro`)
Station coordinates (`stops.txt`) for spatial snapping and track polylines (`shapes.txt`) for Leaflet map rendering.

### 7.3 BMTC Bus GTFS Static Feed (`gtfs_bmtc`)
Bengaluru bus stop GPS nodes and corridor shapes for multi-modal transit comparison.

### 7.4 OpenWeather API Telemetry
Live rainfall volume %, visibility, and temperature feeds.

### 7.5 OpenStreetMap / OSRM Engine
Base driving distance matrices and road geometry polylines.

### Feature Preprocessing Code Implementation
```python
import pandas as pd
import numpy as np

def preprocess_traffic_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    # Cleans Bangalore traffic dataset and extracts temporal features
    df = raw_df.copy()
    df.dropna(subset=['latitude', 'longitude', 'travel_time'], inplace=True)
    
    # Extract temporal signals
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['is_peak_hour'] = df['hour'].apply(lambda h: 1 if (8 <= h <= 10 or 17 <= h <= 20) else 0)
    
    # Outlier removal via IQR method
    q1 = df['travel_time'].quantile(0.25)
    q3 = df['travel_time'].quantile(0.75)
    iqr = q3 - q1
    df = df[(df['travel_time'] >= q1 - 1.5 * iqr) & (df['travel_time'] <= q3 + 1.5 * iqr)]
    return df
```

---

## 8. 🤖 Machine Learning Architectures (XGBoost & Prophet)

### Travel Time Prediction (XGBoost)
The travel duration $T_{pred}$ is modeled using an ensemble of decision trees trained on spatial features, distance $D$, historical speed $V$, weather factors $W$, and peak hour indicator $P$:

$$T_{pred} = f_{XGB}(D, V, W, P) + \epsilon$$

### 2-Hour Traffic Forecasting (Facebook Prophet)
Traffic congestion $Y(t)$ is decomposed into trend $g(t)$, weekly seasonality $s(t)$, hourly seasonality $h(t)$, and weather regressor $w(t)$:

$$Y(t) = g(t) + s(t) + h(t) + \beta w(t) + \epsilon_t$$

---

## 9. 🍃 ARAI Multi-Modal Emission Equations & Calculations

Vehicle emissions depend non-linearly on speed $v$ (km/h). The specific $CO_2$ emission factor $EF_{CO2}$ (g/km) is calculated using ARAI standard coefficients:

$$EF_{CO2}(v) = \alpha + \frac{\beta}{v} + \gamma \cdot v^2$$

| Mode of Transport | Average Speed $v$ | Emission Factor Equation / Value | Carbon Output Calculation |
| :--- | :--- | :--- | :--- |
| **ICE Private Car** | 25 km/h (Urban) | $140 + \frac{350}{v} + 0.02 v^2 \approx 156.5 \text{ g/km}$ | $D \times 156.5 \text{ g/km}$ |
| **Electric Vehicle (EV)** | 25 km/h | Grid Intensity: $0.82 \text{ kg CO}_2/\text{kWh}$, $0.15 \text{ kWh/km} \Rightarrow 123 \text{ g/km}$ | $D \times 123.0 \text{ g/km}$ |
| **Public Bus** | 18 km/h | $800 \text{ g/km}$ shared across 40 passengers $\Rightarrow 20.0 \text{ g/passenger-km}$ | $D \times 20.0 \text{ g/km}$ |
| **Metro Rail** | 35 km/h (Dedicated) | Electrified grid footprint $\Rightarrow 12.0 \text{ g/passenger-km}$ | $D \times 12.0 \text{ g/km}$ |

---

## 10. ⚙️ System Technical Deep Dive

### 10.1 Spatial Snapping Engine (`routing_service.py` / `gtfs_parser.py`)
To efficiently map origin and destination coordinates to the nearest public transit nodes, the system implements a high-performance spatial snapping engine using `scipy.spatial.cKDTree`. By building a k-d tree from the exact GPS nodes located in `stops.txt` (from both the BMRCL Metro and BMTC Bus GTFS static feeds), the backend can resolve nearest-neighbor lookups in `<2ms`, ensuring instantaneous multi-modal routing comparisons.

### 10.2 Polyline Extraction & Map Rendering
Accurate visualization of transit corridors is critical for user pre-trip evaluation. The `gtfs_parser.py` extracts geographic shape sequences from `shapes.txt` corresponding to specific metro lines and bus routes. These sequence coordinates are parsed, sorted, and transmitted as GeoJSON polyline layers via the REST API to the React frontend, where they are dynamically rendered onto Leaflet maps.

---

## 11. 🔍 Explainable AI (SHAP) Diagnostics

TreeSHAP computes exact Shapley values to explain prediction $f(x)$ relative to expected base value $E[f(X)]$:

$$f(x) = E[f(X)] + \sum_{i=1}^{M} \phi_i$$

Where $\phi_i$ represents the impact of feature $i$ (e.g., rainfall, peak hour traffic) on total delay prediction.

```python
import shap

def generate_shap_explanation(model, feature_matrix):
    # Calculates TreeSHAP feature attributions for delay analysis
    explainer = shap.TreeExplainer(model)
    shap_values = explainer(feature_matrix)
    return {
        "base_value": float(explainer.expected_value),
        "feature_attributions": dict(zip(feature_matrix.columns, shap_values.values[0].tolist()))
    }
```

---

## 12. 🌐 API REST Gateway Specifications & OpenAPI Schemas

### Route Recommendation Endpoint
* **URL:** `POST /api/v1/recommend-route`
* **Content-Type:** `application/json`

#### Request Payload
```json
{
  "origin": {"lat": 12.9716, "lng": 77.5946},
  "destination": {"lat": 12.9352, "lng": 77.6245},
  "intended_departure": "2026-10-15T08:30:00Z"
}
```

#### Response Payload
```json
{
  "status": "success",
  "distance_km": 8.4,
  "weather": {"condition": "Moderate Rain", "rainfall_mm": 4.2, "temperature_c": 24.5},
  "routes": [
    {
      "mode": "Metro",
      "duration_min": 22.0,
      "co2_emissions_kg": 0.10,
      "estimated_cost_inr": 30.0,
      "recommendation_score": 94.5
    },
    {
      "mode": "ICE_Car",
      "duration_min": 38.5,
      "co2_emissions_kg": 1.31,
      "estimated_cost_inr": 110.0,
      "recommendation_score": 62.0
    }
  ],
  "shap_explanation": {
    "traffic_density_impact_min": +11.2,
    "rainfall_impact_min": +4.8,
    "baseline_duration_min": 22.5
  }
}
```

---

## 13. 🖥️ Frontend Architecture & React Component Tree

The frontend is built using React.js, Tailwind CSS, Leaflet.js, and Plotly.js.

```
App.jsx (Main Dashboard)
├── Header.jsx (SKIT branding & live system status)
├── RoutingForm.jsx (Origin/Destination inputs with OSRM autocomplete)
├── MapView.jsx (Leaflet interactive map with mode-based color polylines)
├── ModalComparison.jsx (Grid of recommendation cards comparing Metro, EV, Bus, ICE)
└── ShapChart.jsx (Plotly horizontal bar chart rendering SHAP delay drivers)
```

---

## 14. 🤖 Automated Weekly Progress Report System (Form-3 PDF)

To satisfy SKIT Jaipur academic monitoring requirements, the repository includes an automated reporting pipeline:
* **Script:** `generate_report.py` at the repository root parses Git commit history via `git log`.
* **Workflow:** `.github/workflows/auto_weekly_report.yml` executes automatically every Thursday at 11:59 PM IST (or on manual trigger).
* **Output:** Formatted PDF saved to `weekly_reports/` containing metadata, individual contribution metrics (commits, net LOC, active days), trend charts, detailed commit logs, and signature blocks.

---

## 15. 🔀 Git Branching & 1–2 Week Merge Protocol

1. **`main`**: Protected branch containing clean, verified production code.
2. **`backend-dev`**: Dedicated working branch for Nishchal Jain (`/backend`).
3. **`frontend-dev`**: Dedicated working branch for Tanvi Sharma (`/frontend`).
4. **Integration Cadence:** Every 1–2 weeks, developers create a Pull Request (PR) to merge into `main`. The teammate pulls the updated `main` to maintain synchronized local environments.

---

## 16. 🔐 Environment Variables & Security Configuration

Create a `.env` file in `/backend` (never commit this file to Git):

```env
# Backend Environment Settings
PORT=8000
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/smart_transport?retryWrites=true&w=majority
OPENWEATHER_API_KEY=your_openweather_api_key_here
OSRM_BASE_URL=http://router.project-osrm.org
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

---

## 17. 🚀 Step-by-Step Local Setup & Installation Guide

### Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 18. 📐 Developer Guidelines & Modular Interface Contracts

### 18.1 Monorepo Interface Boundaries
To ensure clean collaboration between backend and frontend modules without code duplication or file collisions:
* **Directory Scoping:** Backend engineers work exclusively within `/backend` and root configuration scripts. Frontend engineers work exclusively within `/frontend`.
* **API Schema Locking:** Any modifications to REST request/response structures in `app/api/endpoints.py` MUST be updated in Section 12 of this README before implementation.
* **Shared Types & Constants:** Data field names (e.g., `co2_emissions_kg`, `duration_min`, `shap_explanation`) MUST remain identical across FastAPI Pydantic schemas and React Axios service calls.

### 18.2 Code Style & Quality Standards
* **Python (Backend):** Follow PEP 8 guidelines. Use explicit type hints for all function signatures and Pydantic models for request/response serialization.
* **JavaScript/React (Frontend):** Follow modern ES6+ functional component standards using React Hooks (`useState`, `useEffect`). Utilize Tailwind CSS utility classes for styling.

---

## 19. 🧪 Verification, Testing & Benchmarking Suite

### PyTest Suite Execution
```bash
cd backend
pytest tests/ -v --durations=5
```

### Latency Benchmarking Script
```python
import requests
import time

def benchmark_endpoint(url: str, payload: dict, runs: int = 10):
    durations = []
    for _ in range(runs):
        start = time.perf_counter()
        resp = requests.post(url, json=payload)
        durations.append((time.perf_counter() - start) * 1000)
    print(f"Average Latency: {sum(durations)/runs:.2f} ms")
    print(f"Max Latency: {max(durations):.2f} ms")

if __name__ == "__main__":
    benchmark_endpoint(
        "http://localhost:8000/api/v1/recommend-route",
        {"origin": {"lat": 12.9716, "lng": 77.5946}, "destination": {"lat": 12.9352, "lng": 77.6245}}
    )
```

---

## 20. ❓ Troubleshooting & Frequently Asked Questions

* **Q: What happens if OpenWeather API times out?**
  * *A:* The backend service automatically catches connection timeouts and falls back to historical seasonal weather averages stored in `app/services/weather_service.py`.
* **Q: Why are `.env` files missing from the repository?**
  * *A:* For security best practices, secrets and API keys are excluded via `.gitignore`. Copy `.env.example` to `.env` and fill in your keys locally.
* **Q: How are Form-3 PDF reports archived?**
  * *A:* GitHub Actions automatically triggers `generate_report.py` every Thursday, committing the compiled PDF report directly into the `weekly_reports/` directory.

---
