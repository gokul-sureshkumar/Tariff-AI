import json

# Load the original notebook (not the broken one)
with open(r'C:\CTS Hackathon\Price_Plan_Recommendation-main\Price_Plan_Recommendation-main\notebooks\price_plan_reco_silhouette_fix (2).ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find and fix the problematic cell (cell 20)
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell.get('source', []))
        if 'phone_col = "phone"' in source:
            print(f'Fixing cell {i}')
            # Replace the incorrect column name
            lines = source.split('\n')
            for j, line in enumerate(lines):
                if 'phone_col = "phone"' in line:
                    lines[j] = line.replace('phone_col = "phone"', 'phone_col = "phone_number"')
                    print(f'Fixed line: {lines[j]}')
            
            # Save the lines properly
            nb['cells'][i]['source'] = lines
            break

# Save the corrected notebook
output_file = r'C:\CTS Hackathon\Price_Plan_Recommendation-main\Price_Plan_Recommendation-main\notebooks\price_plan_reco_silhouette_fixed_proper.ipynb'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f'Corrected notebook saved as: {output_file}')

# Let's also debug what columns actually exist in the DataFrame
print('\nChecking the column issue in the data...')
import pandas as pd
from pathlib import Path

DATA_PATH = Path(r'C:\CTS Hackathon\Price_Plan_Recommendation-main\Price_Plan_Recommendation-main\data\raw\cdr_dataset.csv')
df = pd.read_csv(DATA_PATH).copy()

print(f"Original columns: {list(df.columns)}")

def normalize(col: str) -> str:
    return col.strip().lower().replace(" ", "_").replace("-", "_").replace(".", "_")

df.rename(columns={c: normalize(c) for c in df.columns}, inplace=True)

print(f"Normalized columns: {list(df.columns)}")
if 'phone' in df.columns:
    print("'phone' column exists")
elif 'phone_number' in df.columns:
    print("'phone_number' column exists")
else:
    print("Neither 'phone' nor 'phone_number' columns exist!")
