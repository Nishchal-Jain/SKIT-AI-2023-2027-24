import React, { useState } from 'react';
import Header from './components/Header';
import RoutingForm from './components/RoutingForm';
import MapView from './components/MapView';
import ModalComparison from './components/ModalComparison';
import ShapChart from './components/ShapChart';

export default function App() {
  const [routeInfo, setRouteInfo] = useState(null);

  function handleRouteCalculated(data) {
    setRouteInfo(data);
  }

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <Header />

      <main className="flex-1 max-w-7xl w-full mx-auto p-4 md:p-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-1">
            <RoutingForm onRouteCalculated={handleRouteCalculated} />
          </div>

          <div className="lg:col-span-2">
            <MapView routeInfo={routeInfo} />
          </div>
        </div>

        <ModalComparison />
        <ShapChart />
      </main>
    </div>
  );
}