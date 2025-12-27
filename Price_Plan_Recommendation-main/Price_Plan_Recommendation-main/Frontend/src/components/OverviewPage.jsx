import React from 'react';
import { Phone, TrendingUp, Users, Shield, MessageCircle, BarChart3, ShieldCheck } from 'lucide-react';
import './OverviewPage.css';

function OverviewPage({ onGetStarted }) {
  const features = [
    {
      icon: <TrendingUp />,
      title: "Smart Recommendations",
      description: "AI-powered analysis to find your perfect tariff plan based on usage patterns"
    },
    {
      icon: <BarChart3 />,
      title: "Usage Analytics",
      description: "Comprehensive insights into your calling habits and spending patterns"
    },
    {
      icon: <MessageCircle />,
      title: "AI Assistant",
      description: "24/7 chatbot support to help you understand plans and get personalized advice"
    },
    {
      icon: <Shield />,
      title: "Cost Optimization",
      description: "Prevent overspending with intelligent alerts and plan switching recommendations"
    },
    {
      icon: <Users />,
      title: "Multi-Role Support",
      description: "Separate dashboards for customers and telecom administrators"
    },
    {
      icon: <ShieldCheck />,
      title: "Churn Guard",
      description: "Shows the percentage of customers at risk of churn. Helps track potential customer loss easily"
    }
  ];

   return (
    <div className="overview-page">
      {/* Professional Header */}
      <header className="main-header">
        <div className="container header-flex">
          <div className="logo1">
            <span style={{ fontWeight: 900, fontSize: "2.0rem", color: "#fff", letterSpacing: "0.5px" }}>
              Tariff<span style={{ color: "#00e0ff" }}>AI</span>
            </span>
          </div>
        </div>
      </header>

      <div className="hero-section">
        <div className="hero-content">
          {/* Chatbot GIF on the left */}
          <div className="hero-visual">
            <img
              src="https://www.binarycode.co.nz/wp-content/uploads/2023/03/AI-ML-Training-and-Support.gif"
              alt="AI Robot Illustration"
              style={{
                borderRadius: "50%",
                background: "#10205a",
                boxShadow: "0 0 40px #00e0ff55"
              }}
            />
          </div>
          {/* Hero content on the right */}
          <div className="hero-text">
            <h1 className="hero-title">
              Find Your Perfect
              <span className="gradient-text"> Tariff Plan</span>
            </h1>
            <p className="hero-description">
              Smart recommendations powered by AI to help you choose the most cost-effective 
              telecom plan based on your actual usage patterns. Save money and stay connected.
            </p>
            <div className="hero-stats">
              <div className="stat">
                <span className="stat-number">90%</span>
                <span className="stat-label">Accuracy</span>
              </div>
              <div className="stat">
                <span className="stat-number">7K+</span>
                <span className="stat-label">Customers</span>
              </div>
              <div className="stat">
                <span className="stat-number">60%</span>
                <span className="stat-label">Average Savings</span>
              </div>
            </div>
            <button className="btn-primary hero-cta" onClick={onGetStarted}>
              Get Started
            </button>
          </div>
        </div>
      </div>

      <div className="features-section">
        <div className="container">
          <div className="section-header">
            <h2>Why Choose Our Tariff Recommender?</h2>
            <p>Discover how our intelligent system helps you make better decisions</p>
          </div>
          <div className="features-grid">
            {features.map((feature, index) => (
              <div key={index} className="feature-card fade-in" style={{animationDelay: `${index * 0.1}s`}}>
                <div className="feature-icon">
                  {feature.icon}
                </div>
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <footer className="footer-cta">
        <div className="container">
          <div className="cta-content">
            <h2>Ready to Optimize Your Tariff Plan?</h2>
            <p>Join thousands of customers who have already saved money with our smart recommendations</p>
            <button className="btn-primary cta-button" onClick={onGetStarted}>
              Get Started Now
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default OverviewPage;