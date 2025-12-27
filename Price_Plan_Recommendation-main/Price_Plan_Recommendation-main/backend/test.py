from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
from bson import ObjectId

# Initialize Flask app
app = Flask(__name__)

# MongoDB Configuration
MONGODB_CONNECTION_STRING = 'mongodb+srv://test:1234@cluster0.6oeuy4o.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
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
    
    # Convert ObjectId to string
    if '_id' in doc:
        doc['_id'] = str(doc['_id'])
    
    return doc

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
            usage_distribution['Low Usage'] += 5
    
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
    
    # Sort by popularity
    top_plans = sorted(plan_recommendations.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # 4. Customer Segments by Cluster (Donut Chart)
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
            'values': [round(v/len(users), 2) for v in call_patterns.values()],  # Average per customer
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
            'labels': [f'Segment {cluster}' for cluster in cluster_distribution.keys()],
            'values': list(cluster_distribution.values()),
            'title': 'Customer Segments Distribution'
        }
    }

@app.route('/api/user', methods=['POST'])
def get_user_by_phone():
    """
    Fetch user data by phone number
    
    Request Body:
    {
        "phone_number": "382-4657"
    }
    
    Response:
    {
        "success": true,
        "data": { user_object },
        "message": "User found successfully"
    }
    """
    try:
        # Check if MongoDB is connected
        if collection is None:
            return jsonify({
                'success': False,
                'error': 'Database connection not initialized',
                'message': 'Internal server error'
            }), 500
        
        # Get JSON data from request
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json',
                'message': 'Invalid request format'
            }), 400
        
        data = request.get_json()
        
        if not data or 'phone_number' not in data:
            return jsonify({
                'success': False,
                'error': 'Phone number is required',
                'message': 'Please provide phone_number in request body'
            }), 400
        
        phone_number = data.get('phone_number')
        
        # Basic validation
        if not phone_number or not isinstance(phone_number, str):
            return jsonify({
                'success': False,
                'error': 'Invalid phone number',
                'message': 'Phone number must be a valid string'
            }), 400
        
        phone_number = phone_number.strip()
        
        # Query MongoDB for user with matching phone number
        user_doc = collection.find_one({'phone_number': phone_number})
        
        if user_doc:
            # User found
            serialized_user = serialize_mongodb_doc(user_doc)
            return jsonify({
                'success': True,
                'data': serialized_user,
                'message': 'User found successfully'
            }), 200
        else:
            # User not found
            return jsonify({
                'success': False,
                'data': None,
                'message': f'No user found with phone number: {phone_number}'
            }), 404
            
    except PyMongoError as e:
        return jsonify({
            'success': False,
            'error': f'Database error: {str(e)}',
            'message': 'Failed to fetch user data'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal error: {str(e)}',
            'message': 'An unexpected error occurred'
        }), 500

if __name__ == '__main__':
    # Initialize MongoDB connection
    if init_mongodb():
        print("Starting Flask server...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("Failed to initialize MongoDB connection. Server not started.")