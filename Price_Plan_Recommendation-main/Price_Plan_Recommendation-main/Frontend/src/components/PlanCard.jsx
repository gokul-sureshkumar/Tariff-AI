import React from 'react';
import { Check, IndianRupee, Star, TrendingDown } from 'lucide-react';
import './PlanCard.css';

function PlanCard({ plan, rank, isRecommended }) {

  const getBackgroundColor = (rank) => {
    switch (rank) {
      case 1:
        return '#FFD700'; // Gold
      case 2:
        return '#C0C0C0'; // Silver
      case 3:
        return '#CD7F32'; // Bronze
      default:
        return '#FFFFFF'; // Default white
    }
  };

  return (
    <div className={`plan-card ${isRecommended ? 'recommended' : ''}`}>
      {/* {plan.badge && (
        <div className="plan-badge">
          <Star size={14} />
          {plan.badge}
        </div>
      )} */}
      
      <div className="plan-rank" style={{ backgroundColor: getBackgroundColor(rank) }}>#{rank}</div>
      
      <div className="plan-header">
        <h3>{plan.name}</h3>
        <div className="plan-price">
          <p>Monthly</p>
          <span className="currency"><IndianRupee/></span>
          <span className="amount">{plan.monthly_price}</span>
          <span className="period">/month</span>
        </div>
        {/* <div className="plan-price">
          <p>Estimated</p>
          <span className="currency"><IndianRupee/></span>
          <span className="amount">{plan.price}</span>
          <span className="period">/month</span> */}
        {/* </div> */}
      </div>
      
      <div className="plan-savings">
        <TrendingDown size={16} />
        <span>Save ₹{plan.savings}/month</span>
      </div>
      
      <div className="plan-features">
        <div className="feature">
          <span className="feature-label">Free day:</span>
          <span className="feature-value">{plan.plan_detail.free_day}</span>
        </div>
        <div className="feature">
          <span className="feature-label">Free Evening:</span>
          <span className="feature-value">{plan.plan_detail.free_eve}</span>
        </div>
        <div className="feature">
          <span className="feature-label">Free Night:</span>
          <span className="feature-value">{plan.plan_detail.free_night}</span>
        </div>
        <div className="feature">
          <span className="feature-label">Free International:</span>
          <span className="feature-value">{plan.plan_detail.free_intl}</span>
        </div>
      </div>
      
      <div className="plan-benefits">
        {plan.features.map((feature, index) => (
          <div key={index} className="benefit">
            <Check size={14} />
            <span>{feature}</span>
          </div>
        ))}
      </div>
      
      <button className="btn-success choose-btn">
        Choose This Plan
      </button>
    </div>
  );
}

export default PlanCard;