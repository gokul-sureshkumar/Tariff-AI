import pandas as pd
import json
from collections import defaultdict

def read_file_smart(file_path):
    """
    Smart file reader that tries different formats and engines.
    """
    print(f"Attempting to read: {file_path}")
    
    # Check if file exists
    import os
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Get file extension
    file_ext = os.path.splitext(file_path)[1].lower()
    
    # Try different reading methods based on extension
    try:
        if file_ext == '.csv':
            print("  -> Reading as CSV file")
            return pd.read_csv(file_path)
        
        elif file_ext in ['.xlsx', '.xls']:
            # Try different engines for Excel files
            engines = ['openpyxl', 'xlrd'] if file_ext == '.xls' else ['openpyxl']
            
            for engine in engines:
                try:
                    print(f"  -> Trying Excel engine: {engine}")
                    return pd.read_excel(file_path, engine=engine)
                except Exception as e:
                    print(f"  -> Engine {engine} failed: {str(e)}")
                    continue
            
            # If Excel engines fail, try reading as CSV
            print("  -> Excel engines failed, trying as CSV...")
            return pd.read_csv(file_path)
        
        else:
            # For unknown extensions, try CSV first, then Excel
            try:
                print("  -> Unknown extension, trying CSV first...")
                return pd.read_csv(file_path)
            except:
                print("  -> CSV failed, trying Excel...")
                return pd.read_excel(file_path, engine='openpyxl')
                
    except Exception as e:
        raise Exception(f"Could not read file {file_path}. Error: {str(e)}")

def load_plans_data(plans_file_path):
    """
    Load plans data and create a lookup dictionary by plan name.
    """
    print("Loading plans data...")
    plans_df = read_file_smart(plans_file_path)
    
    # Clean column names
    plans_df.columns = plans_df.columns.str.strip()
    
    print(f"Plans file shape: {plans_df.shape}")
    print(f"Plans columns: {plans_df.columns.tolist()}")
    
    # Create lookup dictionary
    plans_lookup = {}
    for _, row in plans_df.iterrows():
        plan_name = str(row['plan_name']).strip()
        plans_lookup[plan_name] = {
            'monthly_rental': float(row['monthly_rental']),
            'rate_local_day': float(row['rate_local_day']),
            'rate_local_eve': float(row['rate_local_eve']),
            'rate_local_night': float(row['rate_local_night']),
            'rate_intl': float(row['rate_intl']),
            'free_day': int(row['free_day']),
            'free_eve': int(row['free_eve']),
            'free_night': int(row['free_night']),
            'free_intl': int(row['free_intl'])
        }
    
    print(f"Loaded {len(plans_lookup)} plans into lookup dictionary")
    return plans_lookup

def merge_excel_to_json(file1_path, file2_path, plans_file_path, output_path):
    """
    Merge two Excel files with plan details and convert to JSON format.
    """
    # Read the files
    print("Reading data files...")
    df1 = read_file_smart(file1_path)  # Customer data
    df2 = read_file_smart(file2_path)  # Plan recommendations
    
    # Load plans data
    plans_lookup = load_plans_data(plans_file_path)
    
    print(f"Customer data shape: {df1.shape}")
    print(f"Recommendations shape: {df2.shape}")
    
    # Clean column names
    df1.columns = df1.columns.str.strip()
    df2.columns = df2.columns.str.strip()
    
    # Print column names for debugging
    print("\nCustomer columns:", df1.columns.tolist())
    print("Recommendations columns:", df2.columns.tolist())
    
    # Group plan recommendations by phone_number
    print("Grouping plan recommendations by phone number...")
    plans_by_phone = defaultdict(list)
    
    for _, row in df2.iterrows():
        phone_number = str(row['phone_number']).strip()
        plan_name = str(row['plan_name']).strip()
        
        # Get plan details from lookup
        plan_details = plans_lookup.get(plan_name, {})
        monthly_rental = plan_details.get('monthly_rental', 0.0)
        
        plan_data = {
            "rank": int(row['rank']),
            "plan_name": plan_name,
            "monthly_rental": monthly_rental,  # Added monthly rental
            "estimated_cost": float(row['estimated_cost']),
            "suitability": float(row['suitability']),
            "final_score": float(row['final_score']),
            # Additional plan details for reference
            "plan_details": plan_details
        }
        plans_by_phone[phone_number].append(plan_data)
    
    # Create the final JSON structure
    print("Creating JSON structure...")
    result = []
    
    for index, row in df1.iterrows():
        phone_number = str(row['phone_number']).strip()
        
        # Get recommended plans for this phone number
        recommended_plans = plans_by_phone.get(phone_number, [])
        
        # Sort plans by rank to ensure correct order
        recommended_plans.sort(key=lambda x: x['rank'])
        
        # Create the JSON object for this customer
        customer_data = {
            "unique_id": f"customer_{index + 1}",  # Generate unique customer ID
            "phone_number": phone_number,
            "cluster_label": row.get('Cluster', ''),
            "recommended_plans": recommended_plans,
            "account_length": row.get('account_length', ''),
            "vmail_message": row.get('vmail_message', ''),
            "day_mins": row.get('day_mins', ''),
            "day_calls": row.get('day_calls', ''),
            "day_charge": row.get('day_charge', ''),
            "eve_mins": row.get('eve_mins', ''),
            "eve_calls": row.get('eve_calls', ''),
            "eve_charge": row.get('eve_charge', ''),
            "night_mins": row.get('night_mins', ''),
            "night_calls": row.get('night_calls', ''),
            "night_charge": row.get('night_charge', ''),
            "intl_mins": row.get('intl_mins', ''),
            "intl_calls": row.get('intl_calls', ''),
            "intl_charge": row.get('intl_charge', ''),
            "custserv_calls": row.get('custserv_calls', ''),
            "churn": row.get('churn', ''),
            "total_mins": row.get('total_mins', ''),
            "total_calls": row.get('total_calls', ''),
            "total_charge": row.get('total_charge', ''),
            "day_mins_share": row.get('day_mins_share', ''),
            "eve_mins_share": row.get('eve_mins_share', ''),
            "night_mins_share": row.get('night_mins_share', ''),
            "intl_mins_share": row.get('intl_mins_share', ''),
            "avg_mins_per_call": row.get('avg_mins_per_call', ''),
            "cluster": row.get('Cluster', '')  # Same as cluster_label
        }
        
        result.append(customer_data)
    
    # Write to JSON file
    print(f"Writing to JSON file: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully created JSON file with {len(result)} records")
    
    # Print some statistics
    plans_per_customer = [len(customer['recommended_plans']) for customer in result]
    print(f"Plans per customer - Min: {min(plans_per_customer)}, Max: {max(plans_per_customer)}, Avg: {sum(plans_per_customer)/len(plans_per_customer):.2f}")
    
    # Print plan rental statistics
    print("\n=== Plan Rental Statistics ===")
    all_rentals = []
    for customer in result:
        for plan in customer['recommended_plans']:
            all_rentals.append(plan['monthly_rental'])
    
    if all_rentals:
        print(f"Monthly rentals - Min: {min(all_rentals)}, Max: {max(all_rentals)}, Avg: {sum(all_rentals)/len(all_rentals):.2f}")
    
    return result

def validate_data(data):
    """
    Validate the merged data and print some sample records.
    """
    print(f"\n=== Data Validation ===")
    print(f"Total records: {len(data)}")
    
    if len(data) > 0:
        print(f"\n=== Sample Record ===")
        sample_record = data[0]
        print(f"Phone Number: {sample_record['phone_number']}")
        print(f"Cluster: {sample_record['cluster_label']}")
        print(f"Number of recommended plans: {len(sample_record['recommended_plans'])}")
        
        if sample_record['recommended_plans']:
            first_plan = sample_record['recommended_plans'][0]
            print(f"First plan: {first_plan['plan_name']} (Rank: {first_plan['rank']})")
            print(f"  Monthly Rental: ₹{first_plan['monthly_rental']}")
            print(f"  Estimated Cost: ₹{first_plan['estimated_cost']}")
    
    # Check for missing plans
    missing_plans = [record for record in data if len(record['recommended_plans']) == 0]
    if missing_plans:
        print(f"\nWarning: {len(missing_plans)} customers have no recommended plans")
        print(f"Example phone numbers: {[record['phone_number'] for record in missing_plans[:5]]}")
    
    # Check for plans without rental information
    missing_rental_info = []
    for record in data:
        for plan in record['recommended_plans']:
            if plan['monthly_rental'] == 0.0:
                missing_rental_info.append((record['phone_number'], plan['plan_name']))
    
    if missing_rental_info:
        print(f"\nWarning: {len(missing_rental_info)} plan recommendations have missing rental information")
        print(f"Examples: {missing_rental_info[:5]}")

# Main execution
if __name__ == "__main__":
    # File paths - UPDATE THESE WITH YOUR ACTUAL FILE PATHS
    file1_path = r"C:\Users\look4\Price_Plan_Recommendation_final\data\processed\customers_with_clusters.csv"  # Customer data
    file2_path = r"C:\Users\look4\Price_Plan_Recommendation_final\data\processed\top3_recommendations_ph.csv"  # Plan recommendations
    plans_file_path = r"C:\Users\look4\Price_Plan_Recommendation_final\data\plans_data.csv"  # Plans details (NEW FILE)
    output_path = "merged_customer_data.json"  # Output JSON file path
    
    # Print current working directory to help with file paths
    import os
    print(f"Current working directory: {os.getcwd()}")
    print("Make sure your files are in this directory or provide full paths.")
    
    try:
        # Merge the files
        merged_data = merge_excel_to_json(file1_path, file2_path, plans_file_path, output_path)
        
        # Validate the results
        validate_data(merged_data)
        
        print(f"\n=== Process Complete ===")
        print(f"Output file: {output_path}")
        
    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
        print("Please check the file paths and make sure the files exist.")
        print("Required files:")
        print("  1. Customer data CSV")
        print("  2. Plan recommendations CSV") 
        print("  3. Plans details CSV (NEW)")
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()

# Alternative function if you want to work with uploaded files in a notebook environment
def merge_uploaded_files(df1, df2, plans_df, output_filename="merged_data.json"):
    """
    Alternative function for when you have already loaded DataFrames
    (useful in Jupyter notebooks or when files are already read)
    """
    # Clean column names
    df1.columns = df1.columns.str.strip()
    df2.columns = df2.columns.str.strip()
    plans_df.columns = plans_df.columns.str.strip()
    
    # Create plans lookup dictionary
    plans_lookup = {}
    for _, row in plans_df.iterrows():
        plan_name = str(row['plan_name']).strip()
        plans_lookup[plan_name] = {
            'monthly_rental': float(row['monthly_rental']),
            'rate_local_day': float(row['rate_local_day']),
            'rate_local_eve': float(row['rate_local_eve']),
            'rate_local_night': float(row['rate_local_night']),
            'rate_intl': float(row['rate_intl']),
            'free_day': int(row['free_day']),
            'free_eve': int(row['free_eve']),
            'free_night': int(row['free_night']),
            'free_intl': int(row['free_intl'])
        }
    
    # Group plans by phone number
    plans_by_phone = defaultdict(list)
    
    for _, row in df2.iterrows():
        phone_number = str(row['phone_number']).strip()
        plan_name = str(row['plan_name']).strip()
        
        # Get plan details from lookup
        plan_details = plans_lookup.get(plan_name, {})
        monthly_rental = plan_details.get('monthly_rental', 0.0)
        
        plan_data = {
            "rank": int(row['rank']),
            "plan_name": plan_name,
            "monthly_rental": monthly_rental,
            "estimated_cost": float(row['estimated_cost']),
            "suitability": float(row['suitability']),
            "final_score": float(row['final_score']),
            "plan_details": plan_details
        }
        plans_by_phone[phone_number].append(plan_data)
    
    # Create JSON structure
    result = []
    for index, row in df1.iterrows():
        phone_number = str(row['phone_number']).strip()
        recommended_plans = plans_by_phone.get(phone_number, [])
        recommended_plans.sort(key=lambda x: x['rank'])
        
        customer_data = {
            "unique_id": f"customer_{index + 1}",
            "phone_number": phone_number,
            "cluster_label": row.get('Cluster', ''),
            "recommended_plans": recommended_plans,
            "account_length": row.get('account_length', ''),
            "vmail_message": row.get('vmail_message', ''),
            "day_mins": row.get('day_mins', ''),
            "day_calls": row.get('day_calls', ''),
            "day_charge": row.get('day_charge', ''),
            "eve_mins": row.get('eve_mins', ''),
            "eve_calls": row.get('eve_calls', ''),
            "eve_charge": row.get('eve_charge', ''),
            "night_mins": row.get('night_mins', ''),
            "night_calls": row.get('night_calls', ''),
            "night_charge": row.get('night_charge', ''),
            "intl_mins": row.get('intl_mins', ''),
            "intl_calls": row.get('intl_calls', ''),
            "intl_charge": row.get('intl_charge', ''),
            "custserv_calls": row.get('custserv_calls', ''),
            "churn": row.get('churn', ''),
            "total_mins": row.get('total_mins', ''),
            "total_calls": row.get('total_calls', ''),
            "total_charge": row.get('total_charge', ''),
            "day_mins_share": row.get('day_mins_share', ''),
            "eve_mins_share": row.get('eve_mins_share', ''),
            "night_mins_share": row.get('night_mins_share', ''),
            "intl_mins_share": row.get('intl_mins_share', ''),
            "avg_mins_per_call": row.get('avg_mins_per_call', ''),
            "cluster": row.get('Cluster', '')
        }
        result.append(customer_data)
    
    # Save to JSON
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully created {output_filename} with {len(result)} records")
    return result

# Function to print plan details for debugging
def print_plan_comparison(data, customer_index=0):
    """
    Print detailed plan comparison for a specific customer for debugging.
    """
    if customer_index >= len(data):
        print(f"Customer index {customer_index} is out of range")
        return
    
    customer = data[customer_index]
    print(f"\n=== Plan Details for Customer {customer['unique_id']} ===")
    print(f"Phone: {customer['phone_number']}")
    print(f"Cluster: {customer['cluster_label']}")
    
    for plan in customer['recommended_plans']:
        print(f"\nRank {plan['rank']}: {plan['plan_name']}")
        print(f"  Monthly Rental: ₹{plan['monthly_rental']}")
        print(f"  Estimated Cost: ₹{plan['estimated_cost']}")
        print(f"  Suitability: {plan['suitability']:.3f}")
        print(f"  Final Score: {plan['final_score']:.3f}")
        
        if plan['plan_details']:
            details = plan['plan_details']
            print(f"  Plan Details:")
            print(f"    Day Rate: ₹{details.get('rate_local_day', 0)}/min (Free: {details.get('free_day', 0)} mins)")
            print(f"    Eve Rate: ₹{details.get('rate_local_eve', 0)}/min (Free: {details.get('free_eve', 0)} mins)")
            print(f"    Night Rate: ₹{details.get('rate_local_night', 0)}/min (Free: {details.get('free_night', 0)} mins)")
            print(f"    Intl Rate: ₹{details.get('rate_intl', 0)}/min (Free: {details.get('free_intl', 0)} mins)")

# Enhanced main execution with example usage
if __name__ == "__main__":
    # File paths - UPDATE THESE WITH YOUR ACTUAL FILE PATHS
    file1_path = r"C:\Users\look4\Price_Plan_Recommendation_final\data\processed\customers_with_clusters.csv"  # Customer data
    file2_path = r"C:\Users\look4\Price_Plan_Recommendation_final\data\processed\top3_recommendations_ph.csv"  # Plan recommendations
    plans_file_path = r"C:\Users\look4\Price_Plan_Recommendation_final\data\processed\plan_catalog.csv"  # Plans details (NEW FILE)
    output_path = "merged_customer_data_with_rentals.json"  # Output JSON file path
    
    # Print current working directory to help with file paths
    import os
    print(f"Current working directory: {os.getcwd()}")
    print("Make sure your files are in this directory or provide full paths.")
    
    try:
        # Merge the files
        merged_data = merge_excel_to_json(file1_path, file2_path, plans_file_path, output_path)
        
        # Validate the results
        validate_data(merged_data)
        
        # Print detailed plan comparison for first customer
        print_plan_comparison(merged_data, 0)
        
        print(f"\n=== Process Complete ===")
        print(f"Output file: {output_path}")
        
    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
        print("Please check the file paths and make sure the files exist.")
        print("Required files:")
        print("  1. Customer data CSV")
        print("  2. Plan recommendations CSV") 
        print("  3. Plans details CSV (NEW)")
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()