import requests
import logging
import time

session = requests.Session()

# Required headers for NSE
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) "
        "Gecko/20100101 Firefox/102.0"
    ),
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}

NSE_HOME = "https://www.nseindia.com"
NSE_QUOTE = "https://www.nseindia.com/api/quote-equity?symbol={symbol}&section=financials"


def init_nse_session():
    """Initializes NSE cookies (mandatory)."""
    try:
        session.get(NSE_HOME, headers=HEADERS, timeout=10)
        logging.info("Initialized NSE session cookies")
    except Exception as e:
        logging.error(f"Failed to init NSE session: {e}")


def fetch_financial_data(company_id: str):
    """Fetch NSE financials with full session handling."""
    company_id = company_id.upper()

    # Step 1: Initialize session cookies
    init_nse_session()

    url = NSE_QUOTE.format(symbol=company_id)

    try:
        response = session.get(url, headers=HEADERS, timeout=10)

        if response.status_code != 200:
            logging.warning(f"NSE returned {response.status_code} for {company_id}")
            return {}

        raw = response.json()

        # Financials are inside this field:
        fin = raw.get("financialsData")
        if not fin:
            logging.warning(f"NSE returned empty financials for {company_id}")
            return {}

        return {
            "balance_sheet": fin.get("balanceSheet", {}),
            "profit_loss": fin.get("profitAndLoss", {}),
            "cash_flow": fin.get("cashFlow", {}),
        }

    except Exception as e:
        logging.error(f"Error fetching NSE data for {company_id}: {e}")
        return {}
