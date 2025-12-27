import React from 'react';
import './CostPieChart.css';

function CostPieChart({ usage }) {
  const total = (usage.dayMinutes + usage.eveMinutes + usage.nightMinutes + usage.intlMinutes).toFixed(0);

  if (total === 0) {
    return <div>No usage data available</div>;
  }

  const segments = [
    { 
      label: 'Day Minutes', 
      value: usage.dayMinutes, 
      percentage: (usage.dayMinutes / total * 100).toFixed(1),
      color: '#f59e0b'
    },
    { 
      label: 'Evening Minutes', 
      value: usage.eveMinutes, 
      percentage: (usage.eveMinutes / total * 100).toFixed(1),
      color: '#7c3aed'
    },
    { 
      label: 'Night Minutes', 
      value: usage.nightMinutes, 
      percentage: (usage.nightMinutes / total * 100).toFixed(1),
      color: '#3730a3'
    },
    { 
      label: 'International', 
      value: usage.intlMinutes, 
      percentage: (usage.intlMinutes / total * 100).toFixed(1),
      color: '#16a34a'
    }
  ];

  let cumulativePercentage = 0;

  return (
    <div className="cost-pie-chart">
      <div className="pie-container">
        <svg viewBox="0 0 200 200" className="pie-svg">
          {segments.map((segment, index) => {
            const startAngle = (cumulativePercentage / 100) * 360;
            const endAngle = ((cumulativePercentage + parseFloat(segment.percentage)) / 100) * 360;
            const largeArcFlag = segment.percentage > 50 ? 1 : 0;
            
            const startX = 100 + 80 * Math.cos((startAngle - 90) * Math.PI / 180);
            const startY = 100 + 80 * Math.sin((startAngle - 90) * Math.PI / 180);
            const endX = 100 + 80 * Math.cos((endAngle - 90) * Math.PI / 180);
            const endY = 100 + 80 * Math.sin((endAngle - 90) * Math.PI / 180);
            
            const pathData = [
              `M 100 100`,
              `L ${startX} ${startY}`,
              `A 80 80 0 ${largeArcFlag} 1 ${endX} ${endY}`,
              `Z`
            ].join(' ');
            
            cumulativePercentage += parseFloat(segment.percentage);
            
            return (
              <path
                key={index}
                d={pathData}
                fill={segment.color}
                stroke="white"
                strokeWidth="2"
                className="pie-segment"
              />
            );
          })}
        </svg>
        
        <div className="pie-center">
          <span className="center-value">{total}</span>
          <span className="center-label">Total Minutes</span>
        </div>
      </div>
      
      <div className="pie-legend">
        {segments.map((segment, index) => (
          <div key={index} className="legend-item">
            <div 
              className="legend-color" 
              style={{ backgroundColor: segment.color }}
            ></div>
            <div className="legend-text">
              <span className="legend-label">{segment.label}</span>
              <span className="legend-value">{segment.value} min ({segment.percentage}%)</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default CostPieChart;
