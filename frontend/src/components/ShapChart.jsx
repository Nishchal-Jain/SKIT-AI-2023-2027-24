import React from 'react';

export default function ShapChart() {
  const factors = [
    { label: 'Base Travel Time', value: '22.5 min', impact: 'baseline', width: '60%' },
    { label: 'Peak Hour Traffic Surge', value: '+11.2 min delay', impact: 'negative', width: '85%' },
    { label: 'Rainfall / Weather Impact', value: '+4.8 min delay', impact: 'negative', width: '40%' },
  ];

  return (
    <div className="bg-white p-5 rounded-xl shadow-sm border border-slate-200 mt-6">
      <div className="flex justify-between items-center mb-3">
        <h3 className="text-base font-semibold text-slate-800">Explainable AI (SHAP) Decision Transparency</h3>
        <span className="text-xs text-emerald-700 bg-emerald-50 font-medium px-2.5 py-1 rounded-full border border-emerald-200">
          XGBoost + SHAP Model
        </span>
      </div>
      <p className="text-xs text-slate-500 mb-4">
        Quantifying exact factors contributing to delay & traffic congestion for full commuter transparency.
      </p>
      <div className="space-y-3">
        {factors.map((f, i) => (
          <div key={i} className="text-xs">
            <div className="flex justify-between mb-1">
              <span className="font-medium text-slate-700">{f.label}</span>
              <span className="font-semibold text-slate-800">{f.value}</span>
            </div>
            <div className="w-full bg-slate-100 rounded-full h-2">
              <div
                className={`h-2 rounded-full ${f.impact === 'negative' ? 'bg-amber-500' : 'bg-emerald-500'}`}
                style={{ width: f.width }}
              ></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}