import pandas as pd
import logging

# Configure logging
logging.basicConfig(
    filename="data_cleaning_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def clean_financial_data(raw_data: dict) -> dict:
    """
    Cleans and normalizes the financial data dictionary.
    - Removes null or empty fields
    - Converts numeric strings to floats
    - Standardizes key names (lowercase, underscores)
    """

    if not isinstance(raw_data, dict):
        logging.error("Invalid data format — expected dictionary")
        return {}

    cleaned_data = {}

    for key, value in raw_data.items():
        if value in (None, "", "NA", "N/A"):
            continue  # skip empty fields

        # normalize key name
        new_key = key.strip().lower().replace(" ", "_")

        # convert numeric strings to float
        if isinstance(value, str):
            try:
                if "%" in value:
                    cleaned_data[new_key] = float(value.replace("%", "").strip()) / 100
                else:
                    cleaned_data[new_key] = float(value.replace(",", "").strip())
            except ValueError:
                cleaned_data[new_key] = value  # keep as string if not numeric
        else:
            cleaned_data[new_key] = value

    return cleaned_data


def prepare_dataset_for_ml(json_list: list) -> pd.DataFrame:
    """
    Converts a list of cleaned JSON dictionaries into a DataFrame
    suitable for ML analysis.
    """
    if not json_list:
        logging.warning("Empty dataset provided for ML preparation.")
        return pd.DataFrame()

    df = pd.DataFrame(json_list)

    # Drop duplicate columns or rows if needed
    df = df.drop_duplicates()

    # Handle missing numeric values
    numeric_cols = df.select_dtypes(include=["float", "int"]).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)

    # Optional: Normalize numeric values (scaling)
    for col in numeric_cols:
        col_max = df[col].max()
        if col_max != 0:
            df[col] = df[col] / col_max

    logging.info("✅ Financial dataset cleaned and normalized for ML.")
    return df
