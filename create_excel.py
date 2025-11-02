import pandas as pd

data = [
    ["RELIANCE", "Reliance Industries Ltd", "Energy"],
    ["TCS", "Tata Consultancy Services Ltd", "IT"],
    ["HDFCBANK", "HDFC Bank Ltd", "Banking"],
    ["ICICIBANK", "ICICI Bank Ltd", "Banking"],
    ["INFY", "Infosys Ltd", "IT"],
    ["ITC", "ITC Ltd", "FMCG"],
    ["KOTAKBANK", "Kotak Mahindra Bank Ltd", "Banking"],
    ["LT", "Larsen & Toubro Ltd", "Infrastructure"],
    ["SBIN", "State Bank of India", "Banking"],
    ["BHARTIARTL", "Bharti Airtel Ltd", "Telecom"],
    ["HINDUNILVR", "Hindustan Unilever Ltd", "FMCG"],
    ["AXISBANK", "Axis Bank Ltd", "Banking"],
    ["MARUTI", "Maruti Suzuki India Ltd", "Automobile"],
    ["BAJFINANCE", "Bajaj Finance Ltd", "Financial Services"],
    ["HCLTECH", "HCL Technologies Ltd", "IT"],
    ["ASIANPAINT", "Asian Paints Ltd", "Consumer"],
    ["SUNPHARMA", "Sun Pharmaceutical Industries Ltd", "Pharma"],
    ["TITAN", "Titan Company Ltd", "Consumer"],
    ["ADANIENT", "Adani Enterprises Ltd", "Conglomerate"],
    ["ADANIGREEN", "Adani Green Energy Ltd", "Energy"],
    ["ULTRACEMCO", "UltraTech Cement Ltd", "Cement"],
    ["NESTLEIND", "Nestle India Ltd", "FMCG"],
    ["WIPRO", "Wipro Ltd", "IT"],
    ["POWERGRID", "Power Grid Corporation of India Ltd", "Energy"],
    ["NTPC", "NTPC Ltd", "Energy"]
]

df = pd.DataFrame(data, columns=["Company_ID", "Company_Name", "Sector"])
df.to_excel("Nifty100Companies.xlsx", index=False)
print("✅ Nifty100Companies.xlsx created successfully!")
