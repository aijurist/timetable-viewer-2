import pandas as pd
import json

# Read CSV files
theory_schedule = pd.read_csv('theory_schedule.csv')
lab_schedule = pd.read_csv('lab_schedule.csv')

# Convert to JSON with proper formatting
theory_json = theory_schedule.to_json(orient='records', indent=4, force_ascii=False)
lab_json = lab_schedule.to_json(orient='records', indent=4, force_ascii=False)

# Write to JSON files
with open('theory_schedule.json', 'w', encoding='utf-8') as f:
    f.write(theory_json)

with open('lab_schedule.json', 'w', encoding='utf-8') as f:
    f.write(lab_json)

print("CSV files successfully converted to JSON!")
print(f"Theory schedule: {len(theory_schedule)} records")
print(f"Lab schedule: {len(lab_schedule)} records")