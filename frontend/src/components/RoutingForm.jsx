import React, { useState } from 'react';

export default function RoutingForm() {
  const [origin, setOrigin] = useState('');
  const [destination, setDestination] = useState('');

  return (
    <div className="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
      <h2 className="text-lg font-semibold text-slate-800 mb-4">Plan Your Eco-Friendly Route</h2>
      <form className="space-y-4" onSubmit={(e) => e.preventDefault()}>
        <div>
          <label className="block text-xs font-medium text-slate-500 mb-1">Source Location</label>
          <input
            type="text"
            placeholder="e.g., Majestic, Bengaluru"
            value={origin}
            onChange={(e) => setOrigin(e.target.value)}
            className="w-full p-2.5 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 outline-none"
          />
        </div>
        <div>
          <label className="block text-xs font-medium text-slate-500 mb-1">Destination Location</label>
          <input
            type="text"
            placeholder="e.g., Indiranagar, Bengaluru"
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
            className="w-full p-2.5 text-sm border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 outline-none"
          />
        </div>
        <button
          type="submit"
          className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-2.5 rounded-lg transition-colors text-sm"
        >
          Calculate Route & Emissions
        </button>
      </form>
    </div>
  );
}