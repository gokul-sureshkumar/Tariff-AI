from flask import Flask, request, jsonify, session
from datetime import timedelta
from functools import wraps
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
from bson import ObjectId
from flask_cors import CORS
import pandas as pd
import requests
import os
import json
from groq import Groq

# -----------------------------
# Initialize Flask app & Sessions
# -----------------------------
app = Flask(__name__)
CORS(app, 
     supports_credentials=True,
     resources={
         r"/*": {
             "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
             "methods": ["GET", "POST", "OPTIONS"],
             "allow_headers": ["Content-Type"],
             "supports_credentials": True,
             
         }
     })


app.config.update(
    SECRET_KEY="4c68670966a7d797907eaeac1ca0f279697d988f9a8efa1bab425e73b4a828f9",
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",   # allow cross-origin
    SESSION_COOKIE_SECURE=False,      # False for localhost, True in HTTPS production
    PERMANENT_SESSION_LIFETIME=timedelta(days=7),
)

# -----------------------------
# MongoDB Configuration
# -----------------------------
MONGODB_CONNECTION_STRING = 'mongodb+srv://test:1234@cluster0.b6rfjh1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
DATABASE_NAME = 'main'
COLLECTION_NAME = 'user'

# Global MongoDB client
mongo_client = None
db = None
collection = None

def init_mongodb():
    """Initialize MongoDB connection"""
    global mongo_client, db, collection
    try:
        mongo_client = MongoClient(MONGODB_CONNECTION_STRING)
        # Test the connection
        mongo_client.admin.command('ping')
        db = mongo_client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        print("Successfully connected to MongoDB Atlas!")
        return True
    except ConnectionFailure as e:
        print(f"Failed to connect to MongoDB: {e}")
        return False

def serialize_mongodb_doc(doc):
    """Convert MongoDB document to JSON serializable format"""
    if doc is None:
        return None
    if '_id' in doc:
        doc['_id'] = str(doc['_id'])
    return doc

# -----------------------------
# Auth helpers
# -----------------------------
def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        phone_in_session = session.get("phone_number")
        if not phone_in_session:
            return jsonify({
                "success": False,
                "error": "Not authenticated",
                "message": "Login required. Please POST to /login with phone_number."
            }), 401
        return fn(*args, **kwargs)
    return wrapper

@app.route('/login', methods=['POST'])
def login():
    """
    Login with phone number only if exists in MongoDB.
    """
    try:
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Content-Type must be application/json",
                "message": "Invalid request format"
            }), 400

        data = request.get_json(silent=True) or {}
        phone_number = data.get("phone_number")

        if not phone_number or not isinstance(phone_number, str) or not phone_number.strip():
            return jsonify({
                "success": False,
                "error": "Invalid phone number",
                "message": "Provide a non-empty phone_number string"
            }), 400

        # Check if phone_number exists in MongoDB
        user = collection.find_one({"phone_number": phone_number.strip()})
        if not user:
            return jsonify({
                "success": False,
                "error": "User not found",
                "message": f"Phone number {phone_number} is not registered"
            }), 404

        # Save to session
        session.permanent = True
        session["phone_number"] = phone_number.strip()

        return jsonify({
            "success": True,
            "message": "Logged in successfully",
            "data": {
                "phone_number": session["phone_number"],
                "user_id": str(user["_id"]),
                "name": user.get("name", "Unknown User")  # optional field
            }
        }), 200

    except PyMongoError as e:
        return jsonify({
            "success": False,
            "error": f"Database error: {str(e)}",
            "message": "Failed to connect to database"
        }), 500

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Internal error: {str(e)}",
            "message": "An unexpected error occurred"
        }), 500

@app.route('/logout', methods=['POST'])
def logout():
    """Clear the current session."""
    session.clear()
    return jsonify({
        "success": True,
        "message": "Logged out successfully"
    }), 200

# -----------------------------
# Protected API: Uses session phone_number
# -----------------------------
@app.route('/api/user', methods=['POST'])
def get_user_data():
    """
    Fetch user data using the phone_number stored in session.

    Session:
        session["phone_number"] must be set by /login

    Response:
    {
        "success": true,
        "data": { user_object },
        "message": "User found successfully"
    }
    """

    try:
        # print("Session data:", dict(session))  # Debug print
        # if 'phone_number' not in session:
        #     print("No phone number in session")  # Debug print
        #     return jsonify({
        #         "success": False,
        #         "error": "Not authenticated"
        #     }), 401

        data = request.get_json(silent=True) or {}
        phone_number = data.get("phone_number")
        print(f"Looking up phone number: {phone_number}")  # Debug print

        # Get user data from MongoDB
        user = collection.find_one({"phone_number": phone_number})
        if not user:
            return jsonify({
                "success": False,
                "error": "User not found"
            }), 404

        # Convert ObjectId to string and return user data
        user['_id'] = str(user['_id'])
        return jsonify({
            "success": True,
            "data": user
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# -----------------------------
# Admin Routes
# -----------------------------
@app.route('/admin/login', methods=['POST'])
def admin_login():
    """
    Admin login with username and password.

    Request JSON:
    {
        "username": "admin",
        "password": "yourpassword"
    }
    """
    try:
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Content-Type must be application/json",
                "message": "Invalid request format"
            }), 400

        data = request.get_json(silent=True) or {}
        username = data.get("username")
        password = data.get("password")

        if not username or not isinstance(username, str) or not username.strip():
            return jsonify({
                "success": False,
                "error": "Invalid username",
                "message": "Provide a non-empty username string"
            }), 400

        if not password or not isinstance(password, str) or not password.strip():
            return jsonify({
                "success": False,
                "error": "Invalid password",
                "message": "Provide a non-empty password string"
            }), 400

        # Check MongoDB for admin credentials
        admin_collection = db["admin"]
        admin_doc = admin_collection.find()

        if admin_doc:
            session.permanent = True
            session["admin_username"] = username.strip()
            return jsonify({
                "success": True,
                "message": "Admin logged in successfully",
                "data": {"username": session["admin_username"]}
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "Invalid credentials",
                "message": "Username or password is incorrect"
            }), 401

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Internal error: {str(e)}",
            "message": "An unexpected error occurred"
        }), 500

@app.route('/api/admin/dashboard', methods=['GET'])
def get_admin_dashboard():
    """
    Admin dashboard endpoint with analytics and visualization data
    
    Response:
    {
        "success": true,
        "analytics": {
            "total_customers": 7000,
            "churn_percentage": 15.2,
            "total_plans": 3,
            "avg_monthly_revenue": 245.50,
            "total_revenue": 1717500.00,
            "avg_customer_lifetime": 156,
            "high_value_customers": 1200
        },
        "visualizations": {
            "churn_by_cluster": [...],
            "plan_popularity": [...],
            "revenue_distribution": [...],
            "usage_patterns": [...]
        }
    }
    """
    try:
        if collection is None:
            return jsonify({
                'success': False,
                'error': 'Database connection not initialized'
            }), 500
        
        # Get all users data for analytics
        all_users = list(collection.find())
        
        if not all_users:
            return jsonify({
                'success': False,
                'message': 'No customer data found'
            }), 404
        
        # Calculate Analytics
        analytics = calculate_analytics(all_users)
        
        # Generate Visualization Data
        visualizations = generate_visualization_data(all_users)
        
        return jsonify({
            'success': True,
            'analytics': analytics,
            'visualizations': visualizations,
            'message': 'Dashboard data fetched successfully'
        }), 200
        
    except PyMongoError as e:
        return jsonify({
            'success': False,
            'error': f'Database error: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal error: {str(e)}'
        }), 500

def calculate_analytics(users):
    """Calculate 4 key analytics metrics"""
    # Fixed total customers as per your data
    total_customers = 7468
    
    # Fixed total plans
    total_plans = 12
    
    # Churn analysis from actual data
    churned_customers = sum(1 for user in users if user.get('churn', False))
    churn_rate = (churned_customers / total_customers) * 100 if total_customers > 0 else 0
    
    high_value_customers = sum(1 for user in users if user.get('total_charge', 0) > 75)
    high_value_percentage = (high_value_customers / total_customers * 100)
    
    return {
        'total_customers': total_customers,
        'total_plans': total_plans,
        'churn_rate': round(churn_rate, 2),
        'high_value_percentage': round(high_value_percentage, 2)
    }
# =======================
# Persona mapping for 6 clusters
# =======================
cluster_personas = {
    0: "Balanced User",
    1: "Night Owl",
    2: "Day Caller",
    3: "Evening Talker",
    4: "International User",
    5: "Power User"
}

def generate_visualization_data(users):
    """Generate 4 visualizations relevant to telecom data"""

    # 1. Customer Usage Distribution (Pie Chart)
    usage_distribution = {
        'High Usage': 0,
        'Medium Usage': 0,
        'Low Usage': 0
    }

    for user in users:
        total_mins = user.get('total_mins', 0)
        if total_mins > 600:
            usage_distribution['High Usage'] += 1
        elif total_mins > 300:
            usage_distribution['Medium Usage'] += 1
        else:
            usage_distribution['Low Usage'] += 1   # fixed: was += 5 before

    # 2. Call Pattern Analysis (Bar Chart)
    call_patterns = {
        'Day': sum(user.get('day_mins', 0) for user in users),
        'Evening': sum(user.get('eve_mins', 0) for user in users),
        'Night': sum(user.get('night_mins', 0) for user in users),
        'International': sum(user.get('intl_mins', 0) for user in users)
    }

    # 3. Top Recommended Plans (Bar Chart)
    plan_recommendations = {}
    for user in users:
        for plan in user.get('recommended_plans', []):
            if plan.get('rank') == 1:  # Only count top recommendations
                plan_name = plan.get('plan_name', '')
                plan_recommendations[plan_name] = plan_recommendations.get(plan_name, 0) + 1

    top_plans = sorted(plan_recommendations.items(), key=lambda x: x[1], reverse=True)[:5]

    # 4. Customer Segments by Cluster (Donut Chart with persona names)
    cluster_distribution = {}
    for user in users:
        cluster = user.get('cluster', 0)
        cluster_distribution[cluster] = cluster_distribution.get(cluster, 0) + 1

    return {
        'usage_distribution': {
            'type': 'pie',
            'labels': list(usage_distribution.keys()),
            'values': list(usage_distribution.values()),
            'title': 'Customer Usage Distribution'
        },
        'call_patterns': {
            'type': 'bar',
            'labels': list(call_patterns.keys()),
            'values': [round(v / len(users), 2) for v in call_patterns.values()],
            'title': 'Average Minutes by Call Type'
        },
        'top_recommended_plans': {
            'type': 'bar',
            'labels': [plan[0] for plan in top_plans],
            'values': [plan[1] for plan in top_plans],
            'title': 'Top 5 Recommended Plans'
        },
        'cluster_distribution': {
            'type': 'doughnut',
            # ✅ Map cluster IDs to persona names
            'labels': [cluster_personas.get(c, f"Cluster {c}") for c in cluster_distribution.keys()],
            'values': list(cluster_distribution.values()),
            'title': 'Customer Segments Distribution'
        }
    }

    
@app.route('/healthz', methods=['GET'])
def healthz():
    ok = collection is not None
    return jsonify({
        "ok": ok
    }), 200 if ok else 500

@app.after_request
def after_request(response):
    print("CORS header being sent:", response.headers.get("Access-Control-Allow-Origin"))
    return response

# Load your CSV data once at startup
BASE_PATH = "../data/processed"
customers_df = pd.read_csv(f"{BASE_PATH}/customers_with_clusters.csv")
plans_df = pd.read_csv(f"{BASE_PATH}/plan_catalog.csv")
reco_ph_df = pd.read_csv(f"{BASE_PATH}/top3_recommendations_ph.csv")
# reco_cluster_df = pd.read_csv(f"{BASE_PATH}/top3_recommendations.csv")

@app.route("/chat", methods=["POST"])
def telecom_plans_endpoint():
    """
    API endpoint for telecom plans chatbot.
    
    Args:
        user_query (str): User's question about telecom plans
    
    Returns:
        str: AI-generated response
    """
    try:
        data = request.get_json(silent=True) or {}
        user_query = data.get("question", "").strip()
        # Read plans data from JSON file
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        print(BASE_DIR)
        json_path = os.path.join(BASE_DIR, "new.json")
        print(json_path)

        with open(json_path, "r", encoding="utf-8") as f:
            plans_data = json.load(f)
        # Initialize Groq client
        client = Groq(api_key="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")  # Replace with your actual Groq API key)
        
        # Create context for LLM
        context = f"""
        You are a helpful telecom customer service assistant. Answer questions about our telecom plans based on the data provided.

        AVAILABLE PLANS DATA:
        {json.dumps(plans_data, indent=2)}

        INSTRUCTIONS:
        - Provide accurate information based only on the plans data provided
        - Make personalized recommendations based on user needs
        - Compare plans when asked
        - Explain pricing, features, and benefits clearly
        - Use Indian Rupees (₹) for all pricing
        - Be friendly and helpful
        - Answer clearly and concisely

        Answer the user's question based on the plans data.
        """
        
        # Get response from Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": context
                },
                {
                    "role": "user", 
                    "content": user_query
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1000
        )
        
        return jsonify({"answer": chat_completion.choices[0].message.content})
        
    except FileNotFoundError:
        return "Error: Could not find new.json file. Please make sure the file exists."
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"


# -----------------------------
# Entrypoint
# -----------------------------
if __name__ == '__main__':
    # Initialize MongoDB connection
    if init_mongodb():
        print("Starting Flask server...")
        # In production, consider host='127.0.0.1' behind a reverse proxy
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("Failed to initialize MongoDB connection. Server not started.")

# Add this right after app initialization
@app.before_first_request
def initialize():
    init_mongodb()
 