
import React from 'react';
import { Leaf, Activity, MapPinned, Sparkles } from 'lucide-react';

export default function Header() {
  return (
    <header className="app-header">
      <div className="header-inner">

        <a href="/" className="header-brand">
          <div className="header-logo">
            <Leaf size={23} />
          </div>

          <div className="header-brand-text">
            <h1>EcoRoute<span> AI</span></h1>
            <p>SMART SUSTAINABLE MOBILITY</p>
          </div>
        </a>

        <nav className="header-navigation">
          <a href="#planner" className="nav-item active">
            <MapPinned size={16} />
            <span>Route Planner</span>
          </a>

          <a href="#comparison" className="nav-item">
            <Activity size={16} />
            <span>Transport Analysis</span>
          </a>

          <a href="#explainable-ai" className="nav-item">
            <Sparkles size={16} />
            <span>Explainable AI</span>
          </a>
        </nav>

        <div className="header-status">
          <span className="header-status-dot"></span>
          <span>AI Mobility Platform</span>
        </div>

      </div>
    </header>
  );
}
