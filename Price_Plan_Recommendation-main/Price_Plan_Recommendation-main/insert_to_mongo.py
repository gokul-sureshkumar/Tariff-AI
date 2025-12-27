import json
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, BulkWriteError
import os
from typing import List, Dict, Any

def connect_to_mongodb(connection_string: str) -> MongoClient:
    """
    Connect to MongoDB Atlas using connection string
    """
    try:
        client = MongoClient(connection_string)
        # Test the connection
        client.admin.command('ping')
        print("Successfully connected to MongoDB Atlas!")
        return client
    except ConnectionFailure as e:
        print(f"Failed to connect to MongoDB: {e}")
        return None

def insert_customer_data(client: MongoClient, database_name: str, customers_data: List[Dict[Any, Any]]) -> bool:
    """
    Insert customer data into MongoDB Atlas
    """
    try:
        # Access database and collection
        db = client[database_name]
        collection = db["user"]
        
        # Insert all documents
        result = collection.insert_many(customers_data)
        
        print(f"Successfully inserted {len(result.inserted_ids)} documents")
        print(f"Inserted IDs: {result.inserted_ids}")
        
        return True
        
    except BulkWriteError as e:
        print(f"Bulk write error occurred: {e.details}")
        return False
    except Exception as e:
        print(f"An error occurred while inserting data: {e}")
        return False

def load_json_data(file_path: str) -> List[Dict[Any, Any]]:
    """
    Load customer data from JSON file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        # Check if data is a list or single object
        if isinstance(data, dict):
            # If it's a single object, convert to list
            data = [data]
        elif not isinstance(data, list):
            raise ValueError("JSON data must be either a list or a single object")
            
        print(f"Successfully loaded {len(data)} customer records from {file_path}")
        return data
        
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in file '{file_path}': {e}")
        return []
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return []

def main():
    # Path to your JSON file
    json_file_path = "merged_customer_data_with_rentals.json"  # Change this to your JSON file path
    
    # Load customer data from JSON file
    customers_data = load_json_data(json_file_path)
    
    if not customers_data:
        print("No data loaded. Exiting...")
        return
    
    # MongoDB Atlas connection string
    # Replace with your actual connection string
    # CONNECTION_STRING = "mongodb://localhost:27017/"
    CONNECTION_STRING = "mongodb+srv://test:1234@cluster0.b6rfjh1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    
    # Or get from environment variable for security
    # CONNECTION_STRING = os.getenv('MONGODB_CONNECTION_STRING')
    
    # Database name
    DATABASE_NAME = "main"  # Replace with your database name
    
    # Connect to MongoDB
    client = connect_to_mongodb(CONNECTION_STRING)
    
    if client:
        # Insert the data
        success = insert_customer_data(client, DATABASE_NAME, customers_data)
        
        if success:
            print("Data insertion completed successfully!")
            
            # Optional: Query to verify the data was inserted
            db = client[DATABASE_NAME]
            collection = db["user"]
            
            print(f"\nTotal documents in 'user' collection: {collection.count_documents({})}")
            
            # Show inserted documents
            print("\nInserted documents:")
            for doc in collection.find({}, {"unique_id": 1, "phone_number": 1}):
                print(f"- ID: {doc['_id']}, Customer: {doc['unique_id']}, Phone: {doc['phone_number']}")
        
        # Close the connection
        client.close()
        print("\nConnection closed.")
    else:
        print("Failed to connect to MongoDB Atlas. Please check your connection string.")

if __name__ == "__main__":
    main()