import React, { useState, useEffect } from 'react';
import { LogOut, Home, DollarSign, IndianRupee } from 'lucide-react';
import PlanCard from './PlanCard';
import UsageChart from './UsageChart';
import CostPieChart from './CostPieChart';
import './CustomerDashboard.css';

function CustomerDashboard({ onLogout }) {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const session = sessionStorage.getItem("user");
    console.log(session);
    
    const fetchUserData = async () => {
      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/api/user`, {
          method: 'POST',
          body: JSON.stringify({ phone_number: JSON.parse(session).phone_number }),
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        const json = await response.json();
        setUserData(json.data); // ✅ correct
        setLoading(false);
      } catch (error) {
        console.error('Error fetching user data:', error);
        setLoading(false);
      }
    };

    fetchUserData();
  }, []);

  if (loading) return <div>Loading dashboard...</div>;
  if (!userData) return <div>No user data available</div>;

  // Extract current usage
  const currentUsage = {
    dayMinutes: userData.day_mins,
    eveMinutes: userData.eve_mins,
    nightMinutes: userData.night_mins,
    intlMinutes: userData.intl_mins,
  };

  const recommendedPlans = userData?.recommended_plans?.map((plan) => {
    let badge = '';
    if (plan.rank === 1) badge = 'Best Value';
    if (plan.rank === 2) badge = 'Most Popular';
    if (plan.rank === 3) badge = 'Budget Friendly';

    return {
      id: plan.rank,
      name: plan.plan_name,
      price: plan.estimated_cost,
      monthly_price: plan.monthly_rental,
      features: [],
      savings: (plan.estimated_cost - plan.monthly_rental).toFixed(2),
      plan_detail: plan.plan_details,
      badge: badge
    };
  });

  return (
    <div className="customer-dashboard">
      {/* Navbar */}
      <nav className="navbar">
        <div className="nav-container">
          <div className="container header-flex">
            <div className="logo">
              <span
                style={{
                  fontWeight: 900,
                  fontSize: '2.0rem',
                  color: '#fff',
                  letterSpacing: '0.5px',
                  cursor: 'pointer'
                }}
              >
                <a href="/">Tariff<span style={{ color: '#00e0ff' }}>AI</span></a>
              </span>
            </div>
          </div>
          <div className="nav-links">
            <a href="#" className="nav-link active">
              <Home size={18} />
              Dashboard
            </a>
            <button className="btn-secondary logout-btn" onClick={onLogout}>
              <LogOut size={18} />
              Logout
            </button>
          </div>
        </div>
      </nav>

      {/* Dashboard Content */}
      <div className="dashboard-content">
        <div className="dashboard-header">
          <div>
            <h1>Welcome back, {userData.phone_number}!</h1>
            <p>Here are your personalized tariff recommendations</p>
          </div>
          {/* {recommendedPlans.length > 0 && (
            <div className="current-savings">
              <IndianRupee size={24} />
              <div>
                <span className="savings-amount">
                  {userData.total_charge}
                </span>
                <span className="savings-label">Potential Monthly Savings</span>
              </div>
            </div>
          )} */}
        </div>

        <div className="dashboard-grid">
          {/* Recommended Plans */}
          <div className="recommendations-section">
            <div className="section-header">
              <h2>Top 3 Recommended Plans</h2>
              <p>Based on your current usage patterns</p>
            </div>
            <div className="plans-grid">
              {recommendedPlans.map((plan, index) => (
                <PlanCard
                  key={plan.rank}
                  plan={plan}
                  rank={plan.id}
                  isRecommended={index === 0}
                />
              ))}
            </div>
          </div>

          {/* Analytics */}
          <div className="analytics-section">
            <div className="charts-grid">
              <div className="card chart-card">
                <h3>Cost Comparison</h3>
                <UsageChart
                  currentUsage={currentUsage}
                  recommendedPlans={recommendedPlans}
                  totalCharge={userData.total_charge}
                />
              </div>
              <div className="card chart-card">
                <h3>Usage Distribution</h3>
                <CostPieChart usage={currentUsage} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CustomerDashboard;