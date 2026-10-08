import React from 'react';
import { Train, Bus, Zap, Car } from 'lucide-react';

export default function ModalComparison() {
  const modes = [
    { name: 'Metro Rail', time: '22 min', co2: '0.10 kg', cost: '₹30', rec: 'Best Eco Choice', color: 'emerald', icon: Train },
    { name: 'Public Bus', time: '30 min', co2: '0.17 kg', cost: '₹25', rec: 'Eco Friendly', color: 'teal', icon: Bus },
    { name: 'Electric Vehicle', time: '28 min', co2: '1.03 kg', cost: '₹45', rec: 'Moderate', color: 'blue', icon: Zap },
    { name: 'ICE Car', time: '38 min', co2: '1.31 kg', cost: '₹110', rec: 'High Carbon', color: 'rose', icon: Car },
  ];

  return (
    <div className="bg-white p-5 rounded-xl shadow-sm border border-slate-200 mt-6">
      <h3 className="text-base font-semibold text-slate-800 mb-3">Multi-Modal Emission & Time Benchmarking</h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {modes.map((m, idx) => {
          const Icon = m.icon;
          return (
            <div key={idx} className="p-4 rounded-lg border border-slate-200 bg-slate-50 flex flex-col justify-between">
              <div className="flex justify-between items-center mb-2">
                <span className="font-bold text-slate-700 text-sm">{m.name}</span>
                <Icon className="w-5 h-5 text-slate-500" />
              </div>
              <div className="space-y-1 text-xs text-slate-600 my-2">
                <p><strong className="text-slate-800">Duration:</strong> {m.time}</p>
                <p><strong className="text-slate-800">CO₂ Output:</strong> {m.co2}</p>
                <p><strong className="text-slate-800">Est. Cost:</strong> {m.cost}</p>
              </div>
              <span className="text-[10px] font-medium px-2 py-1 rounded bg-slate-200 text-slate-700 text-center">
                {m.rec}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}