import pandas as pd
import json
import os
from nifty_financials import fetch_financial_data

# Load Excel and extract company IDs
excel_path = "Nifty100Companies.xlsx"
output_dir = "raw_financial_data"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Read Excel file
df = pd.read_excel(excel_path)

# Ensure there is a column named 'Company_ID' (adjust if different)
company_ids = df["Company_ID"].dropna().astype(str).tolist()

print(f"Found {len(company_ids)} company IDs to process...")

# Loop through IDs and fetch financials
for company_id in company_ids:
    print(f"Fetching data for {company_id}...")
    data = fetch_financial_data(company_id)

    if data:
        # Save raw JSON locally for debugging
        output_path = os.path.join(output_dir, f"{company_id}.json")
        with open(output_path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"✅ Saved data for {company_id}")
    else:
        print(f"⚠️ No valid data for {company_id}")
