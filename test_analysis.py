# test_analysis.py
from analysis_engine import analyze_company

sample = {
    "profit_margin": 0.20,
    "debt_to_equity": 0.25,
    "cash_flow_growth": -0.03,
    "roe": 0.18,
    "operating_margin": 0.08,
    "debt_ratio": 0.02
}

print(analyze_company("TCS", sample))
