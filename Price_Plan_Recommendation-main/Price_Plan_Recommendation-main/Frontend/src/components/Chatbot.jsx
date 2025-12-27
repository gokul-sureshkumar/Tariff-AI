import React, { useState, useRef, useEffect } from 'react';
import { MessageCircle, Send, X, Bot, User } from 'lucide-react';
import './Chatbot.css';

function Chatbot({ userType }) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: userType === 'admin' 
        ? "Hi! I'm your admin assistant. I can help you analyze customer data, plan performance, and system insights. What would you like to know?"
        : "Hello! I'm here to help you find the perfect tariff plan. I can analyze your usage patterns and explain why certain plans work best for you. What's your question?",
      sender: 'bot',
      timestamp: new Date()
    }
  ]);
  const [newMessage, setNewMessage] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const mockResponses = {
    customer: {
      'usage': "Based on your current usage pattern, you use mostly day and evening minutes. The Smart Saver plan would be perfect for you because it offers 200 day minutes and 150 evening minutes, which covers your usage with a buffer, while being more cost-effective than your current plan.",
      'recommendation': "I recommend the Smart Saver plan for three key reasons: 1) It matches your usage pattern perfectly, 2) You'll save $15.50 per month compared to your current plan, 3) It includes data rollover so unused minutes carry forward.",
      'explain': "The Smart Saver plan is recommended because your usage analysis shows you primarily make calls during day (150 min) and evening (120 min) hours. This plan provides 200 day and 150 evening minutes, giving you adequate coverage without paying for excessive night or international minutes you don't use.",
      'why': "This recommendation is based on your historical usage data. The algorithm analyzed 6 months of your calling patterns and found that 85% of your calls happen during day/evening hours. The Smart Saver plan optimizes for this pattern while providing the best value.",
      'cost': "Your current monthly cost is $67.50. With the Smart Saver plan, your projected cost would be $25.99, saving you $41.51 per month or $498.12 annually. This includes all your current usage plus a 15% buffer for peak months."
    },
    admin: {
      'analysis': "Current system metrics show 94.2% customer retention rate, with Premium Plus being the most popular plan (40% adoption). Churn risk is highest among Basic Connect users, suggesting potential for upselling opportunities.",
      'performance': "Plan performance analysis: Premium Plus has highest satisfaction (96%) and lowest churn (2.1%). Smart Saver shows strong growth (+25% new subscribers this month). Basic Connect users show 15% churn risk - consider targeted retention campaigns.",
      'trends': "Usage trends indicate customers are increasing evening minute consumption by 12% quarter-over-quarter. International usage has decreased 8%, suggesting opportunity to create more domestic-focused plans.",
      'revenue': "Monthly revenue is $487,290, up 8% from last month. Average revenue per user is $37.92. Premium Plus contributes 52% of total revenue despite being 40% of customer base, indicating strong value proposition.",
      'customers': "You have 12,847 active customers across 23 different plans. 8,945 customers (69.6%) are on our top 3 recommended plans. 847 customers show medium to high churn risk and may benefit from personalized retention offers."
    }
  };

  const generateResponse = (userMessage) => {
    const message = userMessage.toLowerCase();
    const responses = mockResponses[userType];
    
    for (const keyword in responses) {
      if (message.includes(keyword)) {
        return responses[keyword];
      }
    }
    
    // Default responses
    return userType === 'admin' 
      ? "I can help you with customer analysis, plan performance, revenue insights, usage trends, and churn analysis. What specific metric would you like me to explain?"
      : "I can help you understand your tariff recommendations, explain why certain plans are suggested, and simulate different usage scenarios. What would you like to know about your plans?";
  };

const handleSendMessage = async () => {
  if (!newMessage.trim()) return;

  const userMsg = {
    id: Date.now(),
    text: newMessage,
    sender: 'user',
    timestamp: new Date()
  };

  setMessages(prev => [...prev, userMsg]);
  setNewMessage('');

  try {
    // Call backend API
    const response = await fetch(`${import.meta.env.VITE_API_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ question: newMessage })
    });

    const data = await response.json(); // backend returns plain string
    console.log(data);
    

    const botResponse = {
      id: Date.now() + 1,
      text: data.answer,
      sender: 'bot',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, botResponse]);
  } catch (error) {
    const errorResponse = {
      id: Date.now() + 2,
      text: "⚠️ Sorry, I couldn’t reach the server.",
      sender: 'bot',
      timestamp: new Date()
    };
    setMessages(prev => [...prev, errorResponse]);
  }
};

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className={`chatbot ${isOpen ? 'open' : ''}`}>
      <button 
        className="chatbot-toggle"
        onClick={() => setIsOpen(!isOpen)}
      >
        {isOpen ? <X size={24} /> : <MessageCircle size={24} />}
      </button>

      {isOpen && (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <div className="header-content">
              <Bot size={20} />
              <span>AI Assistant</span>
              <span className="user-type">{userType}</span>
            </div>
            <button className="close-chat" onClick={() => setIsOpen(false)}>
              <X size={18} />
            </button>
          </div>

          <div className="chatbot-messages">
            {messages.map(message => (
              <div key={message.id} className={`message ${message.sender}`}>
                <div className="message-icon">
                  {message.sender === 'bot' ? <Bot size={16} /> : <User size={16} />}
                </div>
                <div className="message-content">
                  <p>{message.text}</p>
                  <span className="message-time">
                    {message.timestamp.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                  </span>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          <div className="chatbot-input">
            <div className="input-container">
              <input
                type="text"
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={userType === 'admin' ? "Ask about analytics, customers, or plans..." : "Ask about plans or usage..."}
                className="message-input"
              />
              <button 
                className="send-btn"
                onClick={handleSendMessage}
                disabled={!newMessage.trim()}
              >
                <Send size={18} />
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Chatbot;