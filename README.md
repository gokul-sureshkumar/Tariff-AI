# TariffAI - Price Plan Recommendation System


## 📖 Table of Contents
1. [Project Overview](#-project-overview)
2. [Technology Stack](#-technology-stack)
3. [System Architecture](#-system-architecture)
4. [Project Structure](#-project-structure)
5. [Installation & Setup](#-installation--setup)
6. [Configuration](#-configuration)
7. [API Documentation](#-api-documentation)
8. [Data Architecture](#-data-architecture)
9. [Usage Guide](#-usage-guide)
10. [Port Forwarding](#-port-forwarding)
11. [License](#-license)

## 🚀 Project Overview

TariffAI is an intelligent full-stack web application designed to revolutionize telecom customer experience through AI-powered tariff plan recommendations. The system employs advanced machine learning clustering algorithms to analyze customer usage patterns and suggest the most cost-effective plans from a comprehensive catalog.

**Key Objectives:**
- Deliver hyper-personalized tariff plan recommendations based on individual usage patterns
- Reduce customer churn by 25% through data-driven plan optimization
- Empower administrators with comprehensive analytics on customer segments and plan performance
- Provide real-time cost optimization insights through interactive visualizations
- Offer 24/7 AI-powered customer support through intelligent chatbot integration

**Business Impact:**
- 📈 Increase customer retention by 30%
- 💰 Reduce unnecessary customer spending by 15-40%
- 🎯 Improve plan adoption rates through personalized matching
- 📊 Enable data-driven decision making for product teams

## 🛠 Technology Stack

### Frontend Layer
| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Framework | React | 18.3.1 | Component-based UI development |
| Build Tool | Vite | 6.3.5 | Next-generation frontend tooling |
| Styling | CSS | 3.4.1 | Utility-first CSS framework |
| Routing | React Router DOM | 7.8.2 | Declarative client-side routing |
| Icons | Lucide React | 0.344.0 | Beautiful & consistent iconography |
| Charts | Recharts | 2.8.0 | Composable charting library |

### Backend Layer
| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Framework | Flask | 3.0.0 | Lightweight Python web framework |
| Database | MongoDB Atlas | - | Cloud-native document database |
| Driver | PyMongo | 4.6.0 | MongoDB Python adapter |
| Auth | Flask-Login | 0.6.2 | Session management |
| Data Processing | Pandas | 2.0.3 | Data analysis and manipulation |
| AI Integration | Groq API | - | High-performance LLM inference |

### AI & Machine Learning
| Component | Technology | Purpose |
|-----------|------------|---------|
| Clustering | Scikit-learn | Customer segmentation |
| Language Model | Llama-3.3-70B | Natural language processing |
| API | Groq Cloud | High-speed inference |

### Development Tools
| Category | Tools |
|----------|-------|
| Package Management | npm, pip |
| Code Quality | ESLint, Prettier, Flake8 |
| Version Control | Git |
| Containerization | Docker |
| API Testing | Postman, Thunder Client |

## 🏗 System Architecture

### Architecture Diagram


![WhatsApp Image 2025-09-03 at 15 28 37_b17a0db1](https://github.com/user-attachments/assets/83cf241e-4d9f-41df-adbd-df2ba94fc3d3)




### Data Flow Process

```mermaid
sequenceDiagram
    participant User
    participant Frontend as React Frontend
    participant Backend as Flask Backend
    participant DB as MongoDB
    participant ML as ML Engine
    participant AI as Groq API

    User->>Frontend: Enters phone number
    Frontend->>Backend: POST /login {phone}
    Backend->>DB: Query customer data
    DB-->>Backend: Return customer record
    Backend->>ML: Get cluster recommendations
    ML-->>Backend: Return top 3 plans
    Backend->>DB: Get plan details
    DB-->>Backend: Return plan information
    Backend-->>Frontend: User data + recommendations
    Frontend-->>User: Render dashboard

    User->>Frontend: Ask chatbot question
    Frontend->>Backend: POST /chat {message}
    Backend->>AI: Send query with context
    AI-->>Backend: Return AI response
    Backend-->>Frontend: Send response
    Frontend-->>User: Display answer
```

## 📁 Project Structure

### Directory Hierarchy
```
tariffai-project/
├── backend/                    # Flask Application
│   ├── data/
│   │   ├── processed/          # Pre-processed ML data
│   │   │   ├── customers_with_clusters.csv
│   │   │   ├── plan_catalog.csv
│   │   │   ├── new.json
│   │   │   └── ...
│   │   └── model_features.json # Features used for clustering
│   ├── app.py                 # Main Flask application file
│   ├── requirements.txt       # Python dependencies
│   └── .env                  # Environment variables (create)
├── frontend/                  # React Application
│   ├── public/
│   ├── src/
│   │   ├── components/        # Reusable React components
│   │   ├── pages/            # Main page components (Login, Dashboard)
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   └── .env                  # Frontend env variables (create)
└── README.md                 # Project documentation (this file)
```

### Key File Descriptions

| File | Purpose |
|------|---------|
| `backend/app.py` | Flask application entry point |
| `backend/requirements.txt` | Python dependencies list |
| `backend/data/processed/customers_with_clusters.csv` | Customer data with ML clusters |
| `backend/data/processed/top3_recommendations_ph.csv` | Pre-generated recommendations |
| `frontend/src/App.jsx` | Main React application component |
| `frontend/vite.config.js` | Vite build configuration |
| `docker-compose.yml` | Multi-container Docker setup |

## 💻 Installation & Setup

### Prerequisites
- **Python** 3.8+ [Download](https://www.python.org/downloads/)
- **MongoDB Atlas Account** [Sign Up](https://www.mongodb.com/atlas/database)
- **Groq API Account** [Sign Up](https://console.groq.com/)

### Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-organization/tariffai.git
   cd tariffai
   ```

2. **Backend Setup**
   ```bash
   cd backend
   
   # Create virtual environment
   python -m venv venv
   
   # Activate environment (Unix/macOS)
   source venv/bin/activate
   
   # Activate environment (Windows)
   venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Set up environment variables
   cp .env.example .env
   # Edit .env with your actual values
   
   # Initialize database
   python scripts/init_db.py
   
   # Start development server
   python app.py
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   
   # Install dependencies
   npm install
   
   # Set up environment variables
   cp .env.example .env
   
   # Start development server
   npm run dev
   ```

4. **Access Application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:5000

### Docker Setup (Alternative)

```bash
# Using Docker Compose
docker-compose up -d

# Or build manually
docker build -t tariffai-backend ./backend
docker build -t tariffai-frontend ./frontend
```

## ⚙️ Configuration

### Environment Variables

**Backend (.env)**
```ini
# MongoDB Configuration
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/tariffai?retryWrites=true&w=majority
MONGO_DB_NAME=tariffai

# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_very_secure_secret_key_here
PORT=5000

# Security
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

**Frontend (.env)**
```ini
# API Configuration
VITE_API_URL=http://localhost:5000
VITE_APP_NAME=TariffAI

# Feature Flags
VITE_CHATBOT_ENABLED=true
VITE_ANALYTICS_ENABLED=true
```

### Database Configuration

1. **MongoDB Collections:**
   - `users` - Customer information and usage data
   - `plans` - Telecom plan catalog
   - `recommendations` - Pre-calculated plan recommendations
   - `sessions` - User authentication sessions

2. **Indexes to Create:**
   ```javascript
   // On users collection
   db.users.createIndex({ "phone": 1 }, { unique: true });
   db.users.createIndex({ "cluster_id": 1 });
   
   // On plans collection
   db.plans.createIndex({ "plan_id": 1 }, { unique: true });
   db.plans.createIndex({ "category": 1 });
   ```

## 📡 API Documentation

### Base URL
`http://localhost:5000` (Development)  
`https://api.yourdomain.com` (Production)

### Authentication Endpoints

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/api/login` | POST | Customer login | `{ "phone": "string" }` |
| `/api/admin/login` | POST | Admin login | `{ "username": "string", "password": "string" }` |
| `/api/logout` | POST | Logout user | - |

### Customer Endpoints

| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `/api/user` | POST | Get user data | `{ user: {...}, recommendations: [...] }` |
| `/api/user/usage` | GET | Get usage statistics | `{ usage: {...}, trends: [...] }` |

### Admin Endpoints

| Endpoint | Method | Description | Access |
|----------|--------|-------------|--------|
| `/api/admin/dashboard` | GET | Dashboard metrics | Admin only |
| `/api/admin/users` | GET | User list with filters | Admin only |
| `/api/admin/plans` | GET | Plan performance data | Admin only |

### AI Chatbot Endpoints

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/api/chat` | POST | Send message to AI | `{ "message": "string", "history": [...] }` |

### Health & Utility Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/healthz` | GET | Health check |
| `/api/version` | GET | API version info |

### Example API Request

```bash
# Get user data
curl -X POST "http://localhost:5000/api/user" \
  -H "Content-Type: application/json" \
  -d '{"phone": "5550123456"}'

# Response
{
  "status": "success",
  "data": {
    "user": {
      "name": "John Doe",
      "phone": "5550123456",
      "current_plan": "Basic Plan",
      "cluster_id": 3,
      "cluster_name": "Evening Talker",
      "usage_pattern": {
        "total_call_mins": 1245,
        "day_call_mins": 300,
        "evening_call_mins": 500,
        "night_call_mins": 445,
        "international_call_mins": 120,
        "total_sms": 89,
        "total_data_gb": 15.2
      }
    },
    "recommendations": [
      {
        "plan_id": "plan_evening_pro",
        "name": "Evening Pro",
        "price": 349,
        "category": "Mid-Range",
        "estimated_savings": 15.50,
        "match_score": 92,
        "features": {
          "call_mins": 1000,
          "evening_mins": 500,
          "sms": 100,
          "data_gb": 5
        }
      }
    ]
  }
}
```

## 🗃️ Data Architecture

### Customer Clusters (ML Segments)

| Cluster ID | Persona Name | Usage Pattern | Target Plans |
|------------|--------------|---------------|--------------|
| 0 | Balanced User | Even usage across all periods | All-Rounder, Value Plus |
| 1 | Night Owl | 60%+ usage during night | Night Owl, Unlimited Nights |
| 2 | Day Caller | 70%+ usage during daytime | Day Saver, Business Pro |
| 3 | Evening Talker | Peak evening usage | Evening Pro, Socializer |
| 4 | International User | High international calls | Global Connect, World Traveler |
| 5 | Power User | High overall usage volume | Ultra Unlimited, Premium Plus |

### Plan Categories & Pricing

| Category | Price Range | Example Plans | Target Audience |
|----------|-------------|---------------|-----------------|
| Budget | ₹99-199 | Lite Voice, Lite Value, Night Owl | Low-usage customers, students |
| Mid-Range | ₹249-399 | Day Saver, All-Rounder, Global Saver | Average users, professionals |
| Premium | ₹499-599 | Ultra Unlimited, Global Connect | High-value customers, businesses |

### Database Schema

**Users Collection**
```javascript
{
  _id: ObjectId,
  phone: String,           // Unique identifier
  name: String,
  email: String,
  current_plan_id: String, // Reference to plans collection
  cluster_id: Number,      // 0-5 based on ML clustering
  usage_pattern: {
    total_call_mins: Number,
    day_call_mins: Number,
    evening_call_mins: Number,
    night_call_mins: Number,
    international_call_mins: Number,
    total_sms: Number,
    total_data_gb: Number
  },
  churn_risk: String,     // 'Low', 'Medium', 'High'
  value_segment: String,  // 'Low', 'Medium', 'High'
  created_at: Date,
  last_login: Date
}
```

**Plans Collection**
```javascript
{
  _id: ObjectId,
  plan_id: String,        // Unique identifier
  name: String,
  price: Number,
  category: String,       // 'Budget', 'Mid-Range', 'Premium'
  features: {
    call_mins: Number,
    sms: Number,
    data_gb: Number,
    night_unlimited: Boolean,
    international_roaming: Boolean,
    validity_days: Number
  },
  description: String,
  target_clusters: [Number], // Which clusters this plan targets
  popularity_score: Number,  // 0-100 based on adoption
  created_at: Date,
  updated_at: Date
}
```

## 📊 Usage Guide

### For Customers

1. **Accessing the Portal**
   - Navigate to the application URL
   - Enter your registered phone number
   - Click "Login" to access your dashboard

2. **Understanding Your Dashboard**
   - View your current plan and usage statistics
   - See personalized plan recommendations
   - Understand your usage patterns through visualizations

3. **Using the AI Chatbot**
   - Click the chat icon in the bottom right corner
   - Ask questions about plans, billing, or usage
   - Examples: "What's the best plan for international calls?", "How can I reduce my bill?"

### For Administrators

1. **Admin Login**
   - Navigate to the admin login page
   - Use your administrator credentials
   - Access the comprehensive dashboard

2. **Dashboard Overview**
   - View key metrics: Total customers, churn rate, ARPU
   - Monitor plan performance and adoption rates
   - Analyze customer segment distributions

3. **Customer Management**
   - Filter customers by cluster, usage, or risk profile
   - View individual customer details and history
   - Export reports for analysis

### For Developers

1. **API Integration**
   - Use the documented API endpoints
   - Handle authentication via session cookies
   - Implement error handling for all requests

2. **Data Processing**
   - New customer data should be processed through the clustering model
   - Regular updates to plan recommendations
   - Monthly usage data updates


### Performance Optimization

1. **Database Indexing**
   - Ensure proper indexes on frequently queried fields
   - Implement query optimization
   - Set up database connection pooling

2. **Caching Strategy**
   - Implement Redis for session storage
   - Cache frequently accessed data
   - Use CDN for static assets

3. **API Optimization**
   - Implement rate limiting
   - Use pagination for large datasets
   - Enable response compression

## Port Forwarding 

## Overview
Port forwarding has been configured to make the TariffAI application accessible from external networks for demonstration purposes.

### Configuration Details

#### Backend (Flask API)
- **Internal Port**: 5000
- **External Port**: 5000
- **Protocol**: TCP

#### Frontend (React Development Server)
- **Internal Port**: 5173
- **External Port**: 5173
- **Protocol**: TCP

#### Access Instructions

#### Local Network Access
http://[local-ip]:5173

#### External Network Access
http://[public-ip]:5173



## 📄 License

This project is licensed under the LOKESHWAR and his [Team](#developers) - see the [LICENSE](LICENSE) file for details.

### Third-Party Licenses

This project uses several open-source packages:

- **React:** MIT License
- **Flask:** BSD 3-Clause License
- **MongoDB:** Server Side Public License (SSPL)
- **Groq API:** Proprietary, subject to Groq's Terms of Service


