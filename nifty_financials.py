import requests
import logging
import time
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    filename="financials_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- API Settings ---
API_URL = "https://example.com/api/financials"  # 🔁 replace with your actual API endpoint
API_KEY = "YOUR_API_KEY_HERE"  # move this to .env for safety

def fetch_financial_data(company_id: str, retries: int = 3, delay: int = 5) -> Dict[str, Any]:
    """
    Fetch financial data (Balance Sheet, P&L, Cash Flow) for a company ID.
    Includes retry and timeout handling.
    """
    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {"company_id": company_id}

    for attempt in range(1, retries + 1):
        try:
            logging.info(f"Fetching data for Company ID: {company_id} (Attempt {attempt})")
            response = requests.get(API_URL, headers=headers, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                # Validate that all required sections exist
                required_fields = ["balance_sheet", "profit_loss", "cash_flow"]
                if all(field in data for field in required_fields):
                    logging.info(f"✅ Successfully fetched data for {company_id}")
                    return data
                else:
                    logging.warning(f"❗ Missing fields for {company_id}: {data.keys()}")
                    return {}

            elif response.status_code == 404:
                logging.error(f"❌ Company ID {company_id} not found.")
                return {}

            else:
                logging.warning(f"⚠️ API returned {response.status_code} for {company_id}")
        
        except requests.Timeout:
            logging.warning(f"⏳ Timeout for {company_id} (Attempt {attempt})")
        except requests.RequestException as e:
            logging.error(f"💥 Request error for {company_id}: {e}")

        # Wait before retrying
        if attempt < retries:
            time.sleep(delay)

    logging.error(f"🚫 Failed to fetch data for {company_id} after {retries} retries")
    return {}
