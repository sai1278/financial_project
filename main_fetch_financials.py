import pandas as pd
import json
import os

from nifty_financials import fetch_financial_data
from data_cleaner import clean_financial_data, prepare_dataset_for_ml
from pro_con_analyzer import analyze_pros_cons
from save_to_db import save_analysis_to_db
# CLI color printing
from cli_printer import (
    print_header, print_success, print_error,
    print_warning, print_company_header, print_pros_cons
)

# -----------------------------
# Load Excel + Create Directory
# -----------------------------

excel_path = "Nifty100Companies.xlsx"
output_dir = "raw_financial_data"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load Excel
df = pd.read_excel(excel_path)

# Required Columns
if "Company_ID" not in df.columns or "Company_Name" not in df.columns:
    raise Exception("❌ Excel must contain Company_ID and Company_Name columns")

company_ids = df["Company_ID"].dropna().astype(str).tolist()
total = len(company_ids)

print_header(f"Starting Processing for {total} Companies")

cleaned_results = []
final_output = {}

# -----------------------------
# Process Each Company
# -----------------------------

count = 0

for company_id in company_ids:
    count += 1

    # Company Name
    company_name = df[df["Company_ID"] == company_id]["Company_Name"].values[0]

    # CLI Header
    print_company_header(company_name, company_id, count, total)

    try:
        data = fetch_financial_data(company_id)

        # Save raw JSON
        raw_output_path = os.path.join(output_dir, f"{company_id}_raw.json")
        with open(raw_output_path, "w") as raw_file:
            json.dump(data, raw_file, indent=4)

        if not data or len(data.keys()) == 0:
            print_warning(f"No valid financial data received for {company_id}")
            continue

        # ----------------------------------------
        # Cleaning & Normalizing
        # ----------------------------------------
        all_cleaned = {}

        for section, section_data in data.items():
            if isinstance(section_data, dict):
                cleaned_section = clean_financial_data(section_data)
                if cleaned_section:
                    all_cleaned[section] = cleaned_section

        if not all_cleaned:
            print_warning(f"No cleanable data for {company_id}")
            continue

        cleaned_results.append(all_cleaned)

        # Save cleaned JSON
        cleaned_output_path = os.path.join(output_dir, f"{company_id}_cleaned.json")
        with open(cleaned_output_path, "w") as cleaned_file:
            json.dump(all_cleaned, cleaned_file, indent=4)

        # ----------------------------------------
        # PRO/CON ANALYSIS
        # ----------------------------------------
        pros_cons = analyze_pros_cons(all_cleaned)

        # CLI Display Pros & Cons
        print_pros_cons(pros_cons["top_pros"], pros_cons["top_cons"])

        # ----------------------------------------
        # Save to MySQL Database
        # ----------------------------------------
        save_analysis_to_db(company_id, company_name, pros_cons)

        # Add to final JSON output
        final_output[company_id] = {
            "company_name": company_name,
            "cleaned_financials": all_cleaned,
            "pros_cons_analysis": pros_cons
        }

        print_success(f"Completed: {company_id} - {company_name}")

    except Exception as e:
        print_error(f"Error processing {company_id}: {e}")

# -----------------------------
# ML DATASET
# -----------------------------

if cleaned_results:
    ml_ready = prepare_dataset_for_ml(cleaned_results)

    with open("ml_dataset.json", "w") as ml_file:
        json.dump(ml_ready, ml_file, indent=4)

    print_success("ML Dataset Saved → ml_dataset.json")
else:
    print_warning("ML dataset NOT created (no cleaned data).")

# -----------------------------
# FINAL REPORT
# -----------------------------

with open("final_financial_analysis.json", "w") as f:
    json.dump(final_output, f, indent=4)

print_success("📘 Final Analysis Saved → final_financial_analysis.json")
print_header("Processing Completed Successfully!")
