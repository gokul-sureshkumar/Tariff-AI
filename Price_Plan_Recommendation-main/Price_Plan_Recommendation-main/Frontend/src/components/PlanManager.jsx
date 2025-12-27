import React, { useState } from 'react';
import { Plus, Edit, Trash2, Save, X } from 'lucide-react';
import './PlanManager.css';

function PlanManager() {
  const [plans, setPlans] = useState([
    {
      id: 1,
      name: "Smart Saver",
      price: 25.99,
      dayMinutes: 200,
      eveMinutes: 150,
      nightMinutes: 100,
      intlMinutes: 50,
      features: ["Free SMS", "Customer Support", "Data Rollover"],
      active: true
    },
    {
      id: 2,
      name: "Premium Plus",
      price: 45.99,
      dayMinutes: 500,
      eveMinutes: 400,
      nightMinutes: 300,
      intlMinutes: 100,
      features: ["Unlimited SMS", "Premium Support", "5G Access", "International Roaming"],
      active: true
    },
    {
      id: 3,
      name: "Basic Connect",
      price: 19.99,
      dayMinutes: 100,
      eveMinutes: 80,
      nightMinutes: 60,
      intlMinutes: 20,
      features: ["Basic SMS", "Standard Support"],
      active: true
    }
  ]);

  const [showModal, setShowModal] = useState(false);
  const [editingPlan, setEditingPlan] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    price: '',
    dayMinutes: '',
    eveMinutes: '',
    nightMinutes: '',
    intlMinutes: '',
    features: ['']
  });

  const handleAddPlan = () => {
    setEditingPlan(null);
    setFormData({
      name: '',
      price: '',
      dayMinutes: '',
      eveMinutes: '',
      nightMinutes: '',
      intlMinutes: '',
      features: ['']
    });
    setShowModal(true);
  };

  const handleEditPlan = (plan) => {
    setEditingPlan(plan);
    setFormData({
      name: plan.name,
      price: plan.price.toString(),
      dayMinutes: plan.dayMinutes.toString(),
      eveMinutes: plan.eveMinutes.toString(),
      nightMinutes: plan.nightMinutes.toString(),
      intlMinutes: plan.intlMinutes.toString(),
      features: [...plan.features]
    });
    setShowModal(true);
  };

  const handleDeletePlan = (planId) => {
    if (window.confirm('Are you sure you want to delete this plan?')) {
      setPlans(plans.filter(plan => plan.id !== planId));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const planData = {
      ...formData,
      price: parseFloat(formData.price),
      dayMinutes: parseInt(formData.dayMinutes),
      eveMinutes: parseInt(formData.eveMinutes),
      nightMinutes: parseInt(formData.nightMinutes),
      intlMinutes: parseInt(formData.intlMinutes),
      features: formData.features.filter(feature => feature.trim() !== ''),
      active: true
    };

    if (editingPlan) {
      setPlans(plans.map(plan => 
        plan.id === editingPlan.id 
          ? { ...planData, id: editingPlan.id }
          : plan
      ));
    } else {
      setPlans([...plans, { ...planData, id: Date.now() }]);
    }
    
    setShowModal(false);
  };

  const handleFeatureChange = (index, value) => {
    const newFeatures = [...formData.features];
    newFeatures[index] = value;
    setFormData({ ...formData, features: newFeatures });
  };

  const addFeature = () => {
    setFormData({
      ...formData,
      features: [...formData.features, '']
    });
  };

  const removeFeature = (index) => {
    const newFeatures = formData.features.filter((_, i) => i !== index);
    setFormData({ ...formData, features: newFeatures });
  };

  return (
    <div className="plan-manager">
      <div className="manager-header">
        <h2>Manage Tariff Plans</h2>
        <button className="btn-primary add-btn" onClick={handleAddPlan}>
          <Plus size={18} />
          Add New Plan
        </button>
      </div>

      <div className="plans-table-container card">
        <table className="plans-table">
          <thead>
            <tr>
              <th>Plan Name</th>
              <th>Price</th>
              <th>Day Minutes</th>
              <th>Evening Minutes</th>
              <th>Night Minutes</th>
              <th>International</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {plans.map(plan => (
              <tr key={plan.id}>
                <td className="plan-name">{plan.name}</td>
                <td className="plan-price">${plan.price}</td>
                <td>{plan.dayMinutes}</td>
                <td>{plan.eveMinutes}</td>
                <td>{plan.nightMinutes}</td>
                <td>{plan.intlMinutes}</td>
                <td>
                  <span className={`status ${plan.active ? 'active' : 'inactive'}`}>
                    {plan.active ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td>
                  <div className="action-buttons">
                    <button 
                      className="action-btn edit-btn"
                      onClick={() => handleEditPlan(plan)}
                    >
                      <Edit size={16} />
                    </button>
                    <button 
                      className="action-btn delete-btn"
                      onClick={() => handleDeletePlan(plan.id)}
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {showModal && (
        <div className="modal-overlay">
          <div className="modal-content card">
            <div className="modal-header">
              <h3>{editingPlan ? 'Edit Plan' : 'Add New Plan'}</h3>
              <button className="close-btn" onClick={() => setShowModal(false)}>
                <X size={20} />
              </button>
            </div>
            
            <form onSubmit={handleSubmit} className="plan-form">
              <div className="form-row">
                <div className="form-group">
                  <label>Plan Name</label>
                  <input
                    type="text"
                    className="form-control"
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Price ($)</label>
                  <input
                    type="number"
                    step="0.01"
                    className="form-control"
                    value={formData.price}
                    onChange={(e) => setFormData({...formData, price: e.target.value})}
                    required
                  />
                </div>
              </div>
              
              <div className="form-row">
                <div className="form-group">
                  <label>Day Minutes</label>
                  <input
                    type="number"
                    className="form-control"
                    value={formData.dayMinutes}
                    onChange={(e) => setFormData({...formData, dayMinutes: e.target.value})}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Evening Minutes</label>
                  <input
                    type="number"
                    className="form-control"
                    value={formData.eveMinutes}
                    onChange={(e) => setFormData({...formData, eveMinutes: e.target.value})}
                    required
                  />
                </div>
              </div>
              
              <div className="form-row">
                <div className="form-group">
                  <label>Night Minutes</label>
                  <input
                    type="number"
                    className="form-control"
                    value={formData.nightMinutes}
                    onChange={(e) => setFormData({...formData, nightMinutes: e.target.value})}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>International Minutes</label>
                  <input
                    type="number"
                    className="form-control"
                    value={formData.intlMinutes}
                    onChange={(e) => setFormData({...formData, intlMinutes: e.target.value})}
                    required
                  />
                </div>
              </div>
              
              <div className="form-group">
                <label>Features</label>
                <div className="features-list">
                  {formData.features.map((feature, index) => (
                    <div key={index} className="feature-input">
                      <input
                        type="text"
                        className="form-control"
                        placeholder="Enter feature"
                        value={feature}
                        onChange={(e) => handleFeatureChange(index, e.target.value)}
                      />
                      {formData.features.length > 1 && (
                        <button 
                          type="button"
                          className="remove-feature-btn"
                          onClick={() => removeFeature(index)}
                        >
                          <X size={16} />
                        </button>
                      )}
                    </div>
                  ))}
                  <button 
                    type="button" 
                    className="btn-secondary add-feature-btn"
                    onClick={addFeature}
                  >
                    <Plus size={16} />
                    Add Feature
                  </button>
                </div>
              </div>
              
              <div className="modal-actions">
                <button type="button" className="btn-secondary" onClick={() => setShowModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn-primary">
                  <Save size={16} />
                  {editingPlan ? 'Update Plan' : 'Add Plan'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default PlanManager;