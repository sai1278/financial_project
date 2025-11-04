import pandas as pd
import json
import os
from nifty_financials import fetch_financial_data
from data_cleaner import clean_financial_data, prepare_dataset_for_ml

# Load Excel and extract company IDs
excel_path = "Nifty100Companies.xlsx"
output_dir = "raw_financial_data"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Read Excel
df = pd.read_excel(excel_path)
company_ids = df["Company_ID"].dropna().astype(str).tolist()

print(f"Found {len(company_ids)} company IDs to process...")

cleaned_results = []

for company_id in company_ids:
    print(f"Fetching data for {company_id}...")
    data = fetch_financial_data(company_id)

    if data:
        # --- Clean and normalize each section ---
        all_cleaned = {}
        for section, section_data in data.items():
            if isinstance(section_data, dict):
                all_cleaned[section] = clean_financial_data(section_data)
        cleaned_results.append(all_cleaned)

        # Save cleaned data as JSON for debugging
        output_path = os.path.join(output_dir, f"{company_id}_cleaned.json")
        with open(output_path, "w") as f:
            json.dump(all_cleaned, f, indent=4)
        print(f"✅ Cleaned and saved data for {company_id}")
    else:
        print(f"⚠️ No valid data for {company_id}")

# Convert cleaned JSONs into a DataFrame (optional ML prep)
if cleaned_results:
    ml_ready_df = prepare_dataset_for_ml(cleaned_results)
    ml_ready_df.to_csv("cleaned_financials.csv", index=False)
    print("📊 Cleaned dataset saved to cleaned_financials.csv")
