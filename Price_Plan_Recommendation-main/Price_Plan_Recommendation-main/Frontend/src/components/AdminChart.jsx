import React from 'react';
import './AdminChart.css';

function AdminChart({ type, labels = [], values = [] }) {
  if (!labels.length || !values.length) {
    return <div>No data available</div>;
  }

  switch (type) {
    case 'bar':
      return (
        <div className="chart-container">
          <div className="bar-chart">
            {values.map((val, i) => (
              <div key={i} className="bar-item">
                <div className="bar" style={{ height: `${val}px`, backgroundColor: '#667eea' }}></div>
                <span className="bar-label">{labels[i]}</span>
                <span className="bar-value">{val}</span>
              </div>
            ))}
          </div>
        </div>
      );

    case 'pie':
    case 'doughnut':
      const total = values.reduce((a, b) => a + b, 0);
      let cumulative = 0;
      return (
        <div className="chart-container">
          <svg viewBox="0 0 32 32" className="pie-chart">
            {values.map((val, i) => {
              const percent = (val / total) * 100;
              const dashArray = `${percent} ${100 - percent}`;
              const dashOffset = 25 - cumulative;
              cumulative += percent;
              return (
                <circle
                  key={i}
                  r="16"
                  cx="16"
                  cy="16"
                  fill="transparent"
                  strokeWidth="32"
                  strokeDasharray={dashArray}
                  strokeDashoffset={dashOffset}
                  stroke={`hsl(${i * 60}, 70%, 50%)`}
                />
              );
            })}
          </svg>
          <div className="pie-legend">
            {labels.map((label, i) => (
              <div key={i} className="legend-item">
                <div className="legend-color" style={{ background: `hsl(${i * 60}, 70%, 50%)` }}></div>
                <span>{label} ({((values[i] / total) * 100).toFixed(1)}%)</span>
              </div>
            ))}
          </div>
        </div>
      );

    default:
      return <div>Unsupported chart type: {type}</div>;
  }
}

export default AdminChart;
