import React, { useState } from 'react';
import { ArrowLeft, User, Phone, Lock } from 'lucide-react';
import './LoginPage.css';

function LoginPage({ onLogin, onBack }) {
  const [loginType, setLoginType] = useState('customer');
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    phoneNumber: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (loginType === 'customer') {
        // Customer login (Flask backend)
        const response = await fetch(`${import.meta.env.VITE_API_URL}/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            phone_number: formData.phoneNumber
          }),
          credentials: 'include'
        });

        const data = await response.json();

        if (data.success) {
          const userData = {
            role: 'customer',
            phone_number: data.data.phone_number
          };

          onLogin('customer', userData);
          sessionStorage.setItem('user', JSON.stringify(userData));
        } else {
          setError(data.message || 'Login failed');
        }
      } else {
        // Admin login (Flask backend)
        try {
          const response = await fetch(`${import.meta.env.VITE_API_URL}/admin/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              username: formData.username,
              password: formData.password
            }),
            credentials: 'include'
          });

          var data = await response.json();
        } catch (error) {
          console.error('Error admin login', error);
          setError('Unable to connect to server');
          return;
        }

        if (data.success) {
          const userData = {
            role: 'admin',
            name: data.data.username,
            id: Math.random().toString(36).substr(2, 9)
          };

          onLogin('admin', userData);
          sessionStorage.setItem('user', JSON.stringify(userData));
        } else {
          setError(data.message || 'Admin login failed');
        }
      }
    } catch (err) {
      console.error('Login error:', err);
      setError('Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="login-page">
      <div className="login-background">
        <div className="bg-circle circle-1"></div>
        <div className="bg-circle circle-2"></div>
        <div className="bg-circle circle-3"></div>
      </div>

      <div className="login-container">
        <button className="back-btn" onClick={onBack}>
          <ArrowLeft size={20} />
          Back to Home
        </button>

        <div className="login-card card">
          <div className="login-header">
            <h2>Welcome Back</h2>
            <p>Sign in to access your personalized dashboard</p>
          </div>

          <div className="role-selector">
            <button
              className={`role-btn ${loginType === 'customer' ? 'active' : ''}`}
              onClick={() => setLoginType('customer')}
            >
              <User size={20} />
              Customer
            </button>
            <button
              className={`role-btn ${loginType === 'admin' ? 'active' : ''}`}
              onClick={() => setLoginType('admin')}
            >
              <Lock size={20} />
              Admin
            </button>
          </div>

          <form className="login-form" onSubmit={handleSubmit}>
            {loginType === 'admin' ? (
              <>
                <div className="form-group">
                  <label htmlFor="username" style={{ color: '#f2f6f7ff' }}>
                    Username
                  </label>
                  <div className="input-wrapper">
                    <User className="input-icon" size={20} />
                    <input
                      type="text"
                      id="username"
                      name="username"
                      className="form-control"
                      placeholder="Enter your username"
                      value={formData.username}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                </div>
                <div className="form-group">
                  <label htmlFor="password" style={{ color: '#f2f6f7ff' }}>
                    Password
                  </label>
                  <div className="input-wrapper">
                    <Lock className="input-icon" size={20} />
                    <input
                      type="password"
                      id="password"
                      name="password"
                      className="form-control"
                      placeholder="Enter your password"
                      value={formData.password}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                </div>
              </>
            ) : (
              <div className="form-group">
                <label htmlFor="phoneNumber" style={{ color: '#f2f6f7ff' }}>
                  Phone Number
                </label>
                <div className="input-wrapper">
                  <Phone className="input-icon" size={20} />
                  <input
                    type="tel"
                    id="phoneNumber"
                    name="phoneNumber"
                    className="form-control"
                    placeholder="Enter your phone number"
                    value={formData.phoneNumber}
                    onChange={handleInputChange}
                    required
                  />
                </div>
              </div>
            )}

            {error && <p className="error-message">{error}</p>}

            <button
              type="submit"
              className="btn-primary login-btn"
              disabled={loading}
            >
              {loading
                ? 'Signing in...'
                : `Sign In as ${loginType === 'admin' ? 'Admin' : 'Customer'}`}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;