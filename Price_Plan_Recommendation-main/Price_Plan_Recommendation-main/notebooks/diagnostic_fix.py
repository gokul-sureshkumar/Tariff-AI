import json

# Load the notebook
with open(r'C:\CTS Hackathon\Price_Plan_Recommendation-main\Price_Plan_Recommendation-main\notebooks\price_plan_reco_silhouette_fixed_proper.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find the cell with the recommendation code and add debug info
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell.get('source', []))
        if 'phone_col = "phone_number"' in source:
            print(f'Found cell {i} with phone_col definition')
            
            # Split the source into lines
            lines = source.split('\n')
            
            # Find where phone_col is defined and add debug info after it
            for j, line in enumerate(lines):
                if 'phone_col = "phone_number"' in line:
                    # Insert debug lines after the phone_col definition
                    debug_lines = [
                        '',
                        '# DEBUG: Check what columns we have',
                        'print(f"Available columns: {list(df.columns)}")',
                        'print(f"phone_col value: {phone_col}")',
                        'print(f"Does phone_col exist in df? {phone_col in df.columns}")',
                        'if phone_col in df.columns:',
                        '    print(f"Sample values from {phone_col}: {df[phone_col].head().tolist()}")',
                        'else:',
                        '    print(f"ERROR: {phone_col} not found in columns!")',
                        '    # Try to find similar columns',
                        '    phone_cols = [col for col in df.columns if "phone" in col.lower()]',
                        '    print(f"Columns containing phone: {phone_cols}")',
                        ''
                    ]
                    
                    # Insert debug lines
                    lines = lines[:j+1] + debug_lines + lines[j+1:]
                    break
            
            # Update the cell
            nb['cells'][i]['source'] = lines
            break

# Save the notebook with debug info
output_file = r'C:\CTS Hackathon\Price_Plan_Recommendation-main\Price_Plan_Recommendation-main\notebooks\price_plan_reco_debug.ipynb'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f'Debug notebook saved as: {output_file}')
print('\nPlease run this notebook to see what columns are actually available.')
