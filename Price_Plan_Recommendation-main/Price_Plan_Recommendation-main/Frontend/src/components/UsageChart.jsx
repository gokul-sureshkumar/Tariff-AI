import React from 'react';
import './UsageChart.css';

function UsageChart({ currentUsage, recommendedPlans, totalCharge }) {
  if (!recommendedPlans || recommendedPlans.length === 0) {
    return <div>No recommended plans available</div>;
  }

  const currentPlanCost = totalCharge; // current actual monthly spend
  const bestPlanCost = recommendedPlans[0].price; // cheapest recommended plan
  const savings = currentPlanCost - bestPlanCost;

  // Normalize bar heights relative to the highest cost
  const maxCost = Math.max(currentPlanCost, bestPlanCost);
  const currentBarHeight = (currentPlanCost / maxCost) * 100;
  const bestBarHeight = (bestPlanCost / maxCost) * 100;

  return (
    <div className="usage-chart">
      <div className="chart-bars">
        <div className="bar-group">
          <div className="bar-container">
            <div
              className="bar current-bar"
              style={{ height: `${currentBarHeight}%` }}
            ></div>
            <div className="bar-value">${currentPlanCost.toFixed(2)}</div>
          </div>
          <div className="bar-label">Current Plan</div>
        </div>

        <div className="bar-group">
          <div className="bar-container">
            <div
              className="bar recommended-bar"
              style={{ height: `${bestBarHeight}%` }}
            ></div>
            <div className="bar-value">${bestPlanCost.toFixed(2)}</div>
          </div>
          <div className="bar-label">Recommended</div>
        </div>
      </div>

      <div className="savings-indicator">
        <span className="savings-text">
          Potential Savings: {savings > 0 ? `₹${savings.toFixed(2)}` : 'No savings'}
          /month
        </span>
      </div>
    </div>
  );
}

export default UsageChart;