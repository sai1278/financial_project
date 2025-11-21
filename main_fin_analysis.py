import pandas as pd
import os
from main_fetch_financials import fetch_and_clean_all
from analysis_engine import run_financial_analysis
from ml_model import train_ml_model
from save_to_db import save_all_to_mysql
from cli_printer import print_section

EXCEL_PATH = "Nifty100Companies.xlsx"

def main():
    print_section("STEP 1: Loading Company List")
    df = pd.read_excel(EXCEL_PATH)
    company_ids = df["Company_ID"].dropna().astype(str).tolist()
    print(f"Loaded {len(company_ids)} companies")

    print_section("STEP 2: Fetching & Cleaning Financials")
    cleaned_data = fetch_and_clean_all(company_ids)

    print_section("STEP 3: Saving Cleaned Data to MySQL")
    save_all_to_mysql(cleaned_data)

    print_section("STEP 4: Running Financial Analysis")
    analysis_results = run_financial_analysis(cleaned_data)

    print_section("STEP 5: Training ML Model")
    ml_results = train_ml_model(cleaned_data)

    print_section("STEP 6: Exporting Output CSVs")
    pd.DataFrame(cleaned_data).to_csv("cleaned_financials.csv", index=False)
    pd.DataFrame(analysis_results).to_csv("analysis_results.csv", index=False)
    pd.DataFrame(ml_results).to_csv("ml_predictions.csv", index=False)

    print_section("DONE: All steps completed successfully!")

if __name__ == "__main__":
    main()
