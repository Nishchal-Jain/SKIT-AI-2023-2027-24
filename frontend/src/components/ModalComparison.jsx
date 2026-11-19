
import React from 'react';
import {
  Train,
  Bus,
  Zap,
  Car,
  Clock3,
  IndianRupee,
  Leaf,
  ArrowUpRight,
  Gauge,
} from 'lucide-react';

export default function ModalComparison() {
  const modes = [
    {
      name: 'Metro Rail',
      time: '22 min',
      co2: '0.10 kg',
      cost: '₹30',
      rec: 'Best Eco Choice',
      icon: Train,
      type: 'eco',
      description: 'Lowest carbon emission',
    },
    {
      name: 'Public Bus',
      time: '30 min',
      co2: '0.17 kg',
      cost: '₹25',
      rec: 'Eco Friendly',
      icon: Bus,
      type: 'green',
      description: 'Affordable public transport',
    },
    {
      name: 'Electric Vehicle',
      time: '28 min',
      co2: '1.03 kg',
      cost: '₹45',
      rec: 'Moderate',
      icon: Zap,
      type: 'blue',
      description: 'Electric mobility option',
    },
    {
      name: 'ICE Car',
      time: '38 min',
      co2: '1.31 kg',
      cost: '₹110',
      rec: 'High Carbon',
      icon: Car,
      type: 'red',
      description: 'Higher emission option',
    },
  ];

  return (
    <div className="comparison-content">

      <div className="comparison-intro">
        <div>
          <div className="comparison-title-row">
            <div className="comparison-title-icon">
              <Gauge size={20} />
            </div>

            <div>
              <h3>Multi-Modal Transport Analysis</h3>
              <p>
                Compare travel time, estimated cost and environmental impact.
              </p>
            </div>
          </div>
        </div>

        <span className="comparison-count">
          04 Transport Modes
        </span>
      </div>

      <div className="comparison-grid">
        {modes.map((mode, index) => {
          const Icon = mode.icon;

          return (
            <article
              key={mode.name}
              className={`mode-card mode-${mode.type}`}
            >
              <div className="mode-card-top">
                <div className="mode-icon">
                  <Icon size={23} strokeWidth={1.8} />
                </div>

                {index === 0 && (
                  <span className="best-choice">
                    <Leaf size={11} />
                    Best Eco
                  </span>
                )}
              </div>

              <h4>{mode.name}</h4>
              <p className="mode-description">{mode.description}</p>

              <div className="mode-metrics">

                <div className="mode-metric">
                  <Clock3 size={15} />
                  <div>
                    <span>Travel duration</span>
                    <strong>{mode.time}</strong>
                  </div>
                </div>

                <div className="mode-metric">
                  <Leaf size={15} />
                  <div>
                    <span>CO₂ emissions</span>
                    <strong>{mode.co2}</strong>
                  </div>
                </div>

                <div className="mode-metric">
                  <IndianRupee size={15} />
                  <div>
                    <span>Estimated cost</span>
                    <strong>{mode.cost}</strong>
                  </div>
                </div>

              </div>

              <div className="mode-recommendation">
                <span>{mode.rec}</span>
                <ArrowUpRight size={15} />
              </div>
            </article>
          );
        })}
      </div>

      <div className="comparison-footer">
        <Leaf size={16} />
        <span>
          Compare environmental impact before choosing your journey.
        </span>
      </div>

    </div>
  );
}
