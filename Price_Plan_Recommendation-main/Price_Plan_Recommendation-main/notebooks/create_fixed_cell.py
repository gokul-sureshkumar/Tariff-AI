# This script creates a properly working recommendation cell

fixed_cell_code = '''# =============================
# Enhanced Billing + Recommendations (FIXED)
# =============================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def safe_normalize_shares(row):
    """Safely normalize usage shares"""
    keys = ["day_mins_share", "eve_mins_share", "night_mins_share", "intl_mins_share"]
    vals = [max(0, float(row.get(k, 0))) for k in keys]
    s = sum(vals)
    return dict(zip(keys, [0.25, 0.25, 0.25, 0.25] if s <= 0 else [v/s for v in vals]))

def estimate_bill(row, plan):
    """Calculate estimated bill with safeguards"""
    try:
        total = max(row.get("total_mins", 0), 0)
        shares = safe_normalize_shares(row)
        
        # Calculate minutes for each period
        d = shares["day_mins_share"] * total
        e = shares["eve_mins_share"] * total
        n = shares["night_mins_share"] * total
        intl = shares["intl_mins_share"] * total
        
        # Calculate billable minutes (after free minutes)
        d_bill = max(d - float(plan["free_day"]), 0)
        e_bill = max(e - float(plan["free_eve"]), 0)
        n_bill = max(n - float(plan["free_night"]), 0)
        i_bill = max(intl - float(plan["free_intl"]), 0)
        
        # Calculate variable charges
        variable = (
            d_bill * float(plan["rate_local_day"]) +
            e_bill * float(plan["rate_local_eve"]) +
            n_bill * float(plan["rate_local_night"]) +
            i_bill * float(plan["rate_intl"])
        )
        
        return round(float(plan["monthly_rental"]) + variable, 2)
    except Exception as e:
        print(f"Warning: Billing calculation error - {str(e)}")
        return float(plan["monthly_rental"])

def calculate_plan_suitability(row, plan):
    """Calculate plan suitability score (0-1)"""
    try:
        # Get usage patterns
        total = max(row.get("total_mins", 0), 0)
        shares = safe_normalize_shares(row)
        
        # Time distribution match (40%)
        total_free = plan["free_day"] + plan["free_eve"] + plan["free_night"]
        if total_free > 0:
            time_match = 1 - sum([
                abs(shares["day_mins_share"] - (plan["free_day"] / total_free)),
                abs(shares["eve_mins_share"] - (plan["free_eve"] / total_free)),
                abs(shares["night_mins_share"] - (plan["free_night"] / total_free))
            ]) / 3
        else:
            time_match = 0.5
        
        # Usage volume match (30%)
        volume_match = min(1.0, total_free / max(total, 1)) if total > 0 else 0.5
        
        # Special features match (30%)
        special_score = 0.0
        if shares["intl_mins_share"] > 0.05 and plan["free_intl"] > 0:
            special_score += 0.5
        if total > 800 and total_free > 800:
            special_score += 0.5
            
        # Final weighted score
        final_score = (
            0.4 * max(0, time_match) +
            0.3 * volume_match +
            0.3 * special_score
        )
        
        return round(float(np.clip(final_score, 0, 1)), 3)
    except Exception as e:
        print(f"Warning: Suitability calculation error - {str(e)}")
        return 0.0

def recommend_plans(row, catalog_df, n_recommendations=3):
    """Generate diverse plan recommendations"""
    try:
        recommendations = []
        
        # Calculate scores for all plans
        for _, plan in catalog_df.iterrows():
            monthly_cost = estimate_bill(row, plan)
            suitability = calculate_plan_suitability(row, plan)
            
            # Get plan category and price tier
            category = plan["plan_name"].split()[0]
            price_tier = (
                'Budget' if plan["monthly_rental"] < 250 
                else 'Premium' if plan["monthly_rental"] > 400 
                else 'Standard'
            )
            
            recommendations.append({
                "plan_name": plan["plan_name"],
                "category": category,
                "price_tier": price_tier,
                "monthly_cost": monthly_cost,
                "suitability": suitability,
                "final_score": round(0.5 * (1 - min(monthly_cost/1000, 1)) + 0.5 * suitability, 3)
            })
        
        # Convert to DataFrame for easier handling
        recs_df = pd.DataFrame(recommendations)
        
        # Select diverse recommendations
        final_recs = []
        categories_used = set()
        
        # First get the absolute best match
        if not recs_df.empty:
            best = recs_df.nlargest(1, "final_score").iloc[0]
            final_recs.append(best)
            categories_used.add(best["category"])
        
            # Then get plans from different categories
            remaining = recs_df[~recs_df["category"].isin(categories_used)]
            while len(final_recs) < n_recommendations and not remaining.empty:
                next_best = remaining.nlargest(1, "final_score").iloc[0]
                final_recs.append(next_best)
                categories_used.add(next_best["category"])
                remaining = recs_df[~recs_df["category"].isin(categories_used)]
            
            # If we still need more, take best remaining
            remaining = recs_df[~recs_df["plan_name"].isin([r["plan_name"] for r in final_recs])]
            while len(final_recs) < n_recommendations and not remaining.empty:
                next_best = remaining.nlargest(1, "final_score").iloc[0]
                final_recs.append(next_best)
                remaining = remaining[remaining["plan_name"] != next_best["plan_name"]]
        
        return final_recs
        
    except Exception as e:
        print(f"Warning: Recommendation error - {str(e)}")
        return []

# FIXED: Determine the correct phone column name
print("DEBUG: Available columns:", list(df.columns))
phone_col = None
for col in df.columns:
    if 'phone' in col.lower():
        phone_col = col
        break

if phone_col:
    print(f"DEBUG: Using phone column: {phone_col}")
else:
    print("DEBUG: No phone column found, will use index instead")

# Generate recommendations for all customers
print(f"Processing {len(df)} customers...")
recs = []
successful_processes = 0

for idx, row in df.iterrows():
    try:
        recommendations = recommend_plans(row, catalog_df)
        
        # Get phone number safely
        if phone_col and phone_col in df.columns:
            phone = str(row[phone_col]).strip()
        else:
            phone = f"customer_{idx}"
        
        for rank, rec in enumerate(recommendations, 1):
            recs.append({
                "index": idx,
                "phone": phone,
                "cluster": int(row["Cluster"]) if "Cluster" in row else 0,
                "plan_name": rec["plan_name"],
                "category": rec["category"],
                "estimated_cost": round(rec["monthly_cost"], 2),
                "suitability": rec["suitability"],
                "final_score": rec["final_score"],
                "rank": rank
            })
        
        successful_processes += 1
        if successful_processes % 1000 == 0:
            print(f"Processed {successful_processes} customers successfully...")
            
    except Exception as e:
        print(f"Warning: Error processing customer {idx} - {str(e)}")
        continue

print(f"Successfully processed {successful_processes} out of {len(df)} customers")

# Create recommendations DataFrame
recs_df = pd.DataFrame(recs)
print(f"Created recommendations DataFrame with shape: {recs_df.shape}")

# Check if we have any data
if recs_df.empty:
    print("ERROR: No recommendations generated! Check the data and catalog_df.")
else:
    print(f"Recommendations DataFrame columns: {list(recs_df.columns)}")
    
    # Analyze plan distribution
    print("\\nPlan Distribution Analysis:")
    print("-" * 50)
    
    if "plan_name" in recs_df.columns:
        plan_dist = recs_df["plan_name"].value_counts()
        print("\\nRecommendations per plan:")
        print(plan_dist)
        
        # Visualize distribution
        plt.figure(figsize=(12, 6))
        plan_dist.plot(kind='bar')
        plt.title('Distribution of Recommended Plans')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
        
        # Display sample recommendations
        print("\\nSample Recommendations:")
        display(recs_df.head(10))
    else:
        print("ERROR: plan_name column not found in recommendations!")
        print(f"Available columns: {list(recs_df.columns)}")
'''

print("Fixed cell code created. You can copy this into a new cell in your notebook.")
print("\\n" + "="*50)
print("COPY THE FOLLOWING CODE INTO A NEW CELL:")
print("="*50)
print(fixed_cell_code)
