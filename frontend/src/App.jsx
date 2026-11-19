
import React, { useState } from 'react';
import Header from './components/Header';
import RoutingForm from './components/RoutingForm';
import MapView from './components/MapView';
import ModalComparison from './components/ModalComparison';
import ShapChart from './components/ShapChart';
import './App.css';

export default function App() {
  const [routeInfo, setRouteInfo] = useState(null);

  function handleRouteCalculated(data) {
    setRouteInfo(data);
  }

  return (
    <div className="app-shell min-h-screen flex flex-col">
      <Header />

      <main className="dashboard-main flex-1 w-full">

        {/* Dashboard Hero */}
        <section className="dashboard-hero">
          <div className="hero-content">
            <div className="hero-eyebrow">
              <span className="hero-eyebrow-dot"></span>
              AI-POWERED SUSTAINABLE MOBILITY
            </div>

            <h1>
              Move smarter.
              <span> Travel greener.</span>
            </h1>

            <p>
              Plan intelligent journeys, compare transportation modes
              and make environmentally responsible travel decisions
              with real-time insights.
            </p>
          </div>

          <div className="hero-side-card">
            <div className="hero-icon">🌱</div>
            <div>
              <span className="hero-side-label">OUR MISSION</span>
              <h3>Building greener cities</h3>
              <p>Smarter mobility for a sustainable future.</p>
            </div>
          </div>
        </section>

        {/* Route Planning and Map */}
        <section className="dashboard-section">
          <div className="section-heading">
            <div>
              <span className="section-kicker">01 / PLAN YOUR JOURNEY</span>
              <h2>Journey Planner</h2>
              <p>Find an efficient and eco-friendly way to reach your destination.</p>
            </div>

            <span className="section-tag">
              <span className="live-dot"></span>
              Smart Route Planning
            </span>
          </div>

          <div className="planner-grid">
            <div className="planner-form-panel">
              <RoutingForm
                onRouteCalculated={handleRouteCalculated}
              />
            </div>

            <div className="planner-map-panel">
              <div className="panel-heading">
                <div>
                  <span className="panel-overline">EXPLORE YOUR ROUTE</span>
                  <h3>Interactive City Map</h3>
                </div>
                <span className="map-indicator">
                  <span className="live-dot"></span>
                  Map View
                </span>
              </div>

              <div className="map-container">
                <MapView routeInfo={routeInfo} />
              </div>

              <div className="map-footer">
                <span>Powered by OpenStreetMap</span>
                <span>Leaflet Mapping</span>
              </div>
            </div>
          </div>
        </section>

        {/* Traffic Status Legend - Sprint 5 Story 1 */}
        <section className="traffic-guide-section">
          <div className="traffic-guide-heading">
            <div>
              <span className="section-kicker">02 / TRAFFIC INTELLIGENCE</span>
              <h2>Traffic Condition Guide</h2>
              <p>Understand traffic conditions through an intuitive color system.</p>
            </div>
          </div>

          <div className="traffic-guide-grid">
            <div className="traffic-guide-card traffic-green">
              <div className="traffic-guide-top">
                <span className="traffic-circle"></span>
                <span className="traffic-label">LOW TRAFFIC</span>
              </div>
              <h3>Free Flow</h3>
              <p>Green indicates smooth traffic movement.</p>
            </div>

            <div className="traffic-guide-card traffic-yellow">
              <div className="traffic-guide-top">
                <span className="traffic-circle"></span>
                <span className="traffic-label">MODERATE TRAFFIC</span>
              </div>
              <h3>Moderate Flow</h3>
              <p>Yellow indicates increasing traffic density.</p>
            </div>

            <div className="traffic-guide-card traffic-red">
              <div className="traffic-guide-top">
                <span className="traffic-circle"></span>
                <span className="traffic-label">HEAVY TRAFFIC</span>
              </div>
              <h3>Congested</h3>
              <p>Red indicates heavy traffic and possible delays.</p>
            </div>
          </div>
          <p className="traffic-guide-note">
            Color reference for traffic visualization. Live traffic
            classification will be displayed when connected to traffic data.
          </p>
        </section>

        {/* Transport Comparison */}
        <section className="dashboard-section">
          <div className="section-heading">
            <div>
              <span className="section-kicker">03 / SUSTAINABLE MOBILITY</span>
              <h2>Compare Travel Options</h2>
              <p>Evaluate different transportation modes based on time, cost and emissions.</p>
            </div>
          </div>

          <div className="dashboard-panel comparison-panel">
            <ModalComparison />
          </div>
        </section>

        {/* Explainable AI */}
        <section className="dashboard-section">
          <div className="section-heading">
            <div>
              <span className="section-kicker">04 / EXPLAINABLE ARTIFICIAL INTELLIGENCE</span>
              <h2>Understand AI Decisions</h2>
              <p>Explore the factors contributing to travel delays and congestion.</p>
            </div>

            <span className="ai-badge">
              ✦ Explainable AI
            </span>
          </div>

          <div className="dashboard-panel shap-panel">
            <ShapChart />
          </div>
        </section>

        {/* Footer */}
        <footer className="dashboard-footer">
          <div className="footer-brand">
            <span>🌱</span>
            <strong>Smart Sustainable Transport</strong>
          </div>

          <p>
            AI-powered mobility for a cleaner and smarter tomorrow.
          </p>

          <span className="footer-copy">
            © 2026 Smart Sustainable Transport Optimization System
          </span>
        </footer>

      </main>
    </div>
  );
}
