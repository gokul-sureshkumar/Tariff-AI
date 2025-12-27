import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from 'react-router-dom';

import OverviewPage from './components/OverviewPage';
import LoginPage from './components/LoginPage';
import CustomerDashboard from './components/CustomerDashboard';
import AdminDashboard from './components/AdminDashboard';
import Chatbot from './components/Chatbot';
import './App.css';

function App() {
    const [user, setUser] = useState(() => {
      const savedUser = sessionStorage.getItem("user");
      return savedUser ? JSON.parse(savedUser) : null;
    });

  return (
    <Router>
      <AppRoutes user={user} setUser={setUser} />
    </Router>
  );
}

function AppRoutes({ user, setUser }) {
  const navigate = useNavigate();

  const handleLogin = (role, userData) => {
    setUser(userData);
    if (role === 'customer') {
      navigate('/customer');   // ✅ no reload
    } else {
      navigate('/admin');      // ✅ no reload
    }
  };

  const handleLogout = () => {
    setUser(null);
    sessionStorage.removeItem("user");
    navigate('/'); // ✅ go back to overview without reload
  };

  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<OverviewPage onGetStarted={() => navigate('/login')} />} />
        <Route path="/login" element={<LoginPage onLogin={handleLogin} onBack={() => navigate('/')} />} />
        
        {/* Protected routes */}
        <Route 
          path="/customer" 
          element={
            user?.role === 'customer'
              ? <CustomerDashboard user={user} onLogout={handleLogout} />
              : <Navigate to="/login" replace />
          } 
        />
        <Route 
          path="/admin" 
          element={
            user?.role === 'admin'
              ? <AdminDashboard user={user} onLogout={handleLogout} />
              : <Navigate to="/login" replace />
          } 
        />

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>

      {(user?.role === 'customer' || user?.role === 'admin') && (
        <Chatbot userType={user?.role} />
      )}
    </div>
  );
}

export default App;