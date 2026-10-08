import React from 'react';

export default function Header() {
  return (
    <header className="bg-emerald-700 text-white p-4 shadow-md flex justify-between items-center">
      <div>
        <h1 className="text-xl font-bold">🌿 Smart Sustainable Transport</h1>
        <p className="text-xs text-emerald-100">SKIT Jaipur — Pre-Trip Decision Support System</p>
      </div>
      <span className="bg-emerald-800 text-xs px-3 py-1 rounded-full border border-emerald-600">
        Sprint 4: Active
      </span>
    </header>
  );
}