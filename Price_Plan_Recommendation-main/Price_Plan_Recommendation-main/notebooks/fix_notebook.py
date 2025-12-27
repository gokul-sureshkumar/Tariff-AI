import json

# Load the notebook
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
            nb['cells'][i]['source'] = lines
            break

# Save the corrected notebook
output_file = r'C:\CTS Hackathon\Price_Plan_Recommendation-main\Price_Plan_Recommendation-main\notebooks\price_plan_reco_silhouette_fixed.ipynb'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f'Corrected notebook saved as: {output_file}')
