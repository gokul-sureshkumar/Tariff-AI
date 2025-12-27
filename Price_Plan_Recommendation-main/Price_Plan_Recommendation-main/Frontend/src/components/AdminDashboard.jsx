import React, { useState, useEffect } from 'react';
import { LogOut, Users, TrendingUp, DollarSign, BarChart3, IndianRupee } from 'lucide-react';
import AdminChart from './AdminChart';
import PlanManager from './PlanManager';
import './AdminDashboard.css';

function AdminDashboard({ user, onLogout }) {
  const [activeTab, setActiveTab] = useState('overview');
  const [dashboardData, setDashboardData] = useState(null);

  useEffect(() => {
    // Replace with real API call
    const fetchData = async () => {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/admin/dashboard`); 
      const data = await response.json();
      setDashboardData(data);
    };

    fetchData();
  }, []);

  if (!dashboardData) {
    return <div className="loading">Loading dashboard...</div>;
  }

  const { analytics, visualizations } = dashboardData;

  const stats = [
    {
      title: 'Total Customers',
      value: analytics.total_customers.toLocaleString(),
      change: '',
      icon: <Users />,
      color: '#667eea'
    },
    {
      title: 'Churn Rate',
      value: `${analytics.churn_rate}%`,
      change: '',
      icon: <TrendingUp />,
      color: '#ef4444'
    },
    {
      title: 'High Value Customers',
      value: `${analytics.high_value_percentage}%`,
      change: '',
      icon: <IndianRupee />,
      color: '#10b981'
    },
    {
      title: 'Total Plans',
      value: analytics.total_plans,
      change: '',
      icon: <BarChart3 />,
      color: '#f59e0b'
    }
  ];

  return (
    <div className="admin-dashboard">
      <nav className="navbar">
        <div className="nav-container">
          <div className="container header-flex">
            <div className="logo">
              <a href="/">
              <span style={{ fontWeight: 900, fontSize: "2rem", color: "#fff", letterSpacing: "0.5px" }}>
                Tariff<span style={{ color: "#00e0ff" }}>AI</span>
              </span></a>
            </div>
          </div>
          <div className="nav-links">
            <button 
              className={`nav-tab ${activeTab === 'overview' ? 'active' : ''}`}
              onClick={() => setActiveTab('overview')}
            >
              <BarChart3 size={18} />
              Overview
            </button>
            <button 
              className={`nav-tab ${activeTab === 'plans' ? 'active' : ''}`}
              onClick={() => setActiveTab('plans')}
            >
              <BarChart3 size={18} />
              Plans
            </button>
            <button className="btn-secondary logout-btn" onClick={onLogout}>
              <LogOut size={18} />
              Logout
            </button>
          </div>
        </div>
      </nav>

      <div className="admin-content">
        <div className="admin-header">
          <div>
            <h1>Admin Dashboard</h1>
            <p>Welcome back, {user.name}. Here's your system overview.</p>
          </div>
        </div>

        {activeTab === 'overview' && (
          <div className="overview-content">
            <div className="stats-grid">
              {stats.map((stat, index) => (
                <div key={index} className="stat-card card">
                  <div className="stat-icon" style={{ backgroundColor: stat.color }}>
                    {stat.icon}
                  </div>
                  <div className="stat-content">
                    <h3>{stat.value}</h3>
                    <p>{stat.title}</p>
                  </div>
                </div>
              ))}
            </div>

            <div className="charts-section">
              <div className="chart-row">
                <div className="card chart-card">
                  <h3>{visualizations.call_patterns.title}</h3>
                  <AdminChart 
                    type={visualizations.call_patterns.type}
                    labels={visualizations.call_patterns.labels}
                    values={visualizations.call_patterns.values}
                  />
                </div>
                <div className="card chart-card">
                  <h3>{visualizations.usage_distribution.title}</h3>
                  <AdminChart 
                    type={visualizations.usage_distribution.type}
                    labels={visualizations.usage_distribution.labels}
                    values={visualizations.usage_distribution.values}
                  />
                </div>
              </div>
              <div className="chart-row">
                <div className="card chart-card">
                  <h3>{visualizations.cluster_distribution.title}</h3>
                  <AdminChart 
                    type={visualizations.cluster_distribution.type}
                    labels={visualizations.cluster_distribution.labels}
                    values={visualizations.cluster_distribution.values}
                  />
                </div>
                <div className="card chart-card">
                  <h3>{visualizations.top_recommended_plans.title}</h3>
                  <AdminChart 
                    type={visualizations.top_recommended_plans.type}
                    labels={visualizations.top_recommended_plans.labels}
                    values={visualizations.top_recommended_plans.values}
                  />
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'plans' && (
          <div className="plans-content">
            <PlanManager totalPlans={analytics.total_plans} />
          </div>
        )}
      </div>
    </div>
  );
}

export default AdminDashboard;