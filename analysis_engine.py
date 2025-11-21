# analysis_engine.py
from typing import Dict, Any, List, Optional
import math

# Threshold: metrics > 0.10 (10%) → pro, < 0.10 → con
DEFAULT_THRESHOLD = 0.10

# Templates for metrics (adjust as needed)
INSIGHT_TEMPLATES = {
    "profit_margin": {
        "pro":  "Company shows strong profitability with a profit margin of {value}%.",
        "con":  "Low profitability — profit margin is only {value}%.",
    },
    "debt_to_equity": {
        "pro":  "Company maintains a healthy capital structure — low debt-to-equity ratio ({value}).",
        "con":  "High debt burden — debt-to-equity ratio is {value}.",
    },
    "operating_margin": {
        "pro": "Efficient operations with operating margin at {value}%.",
        "con": "Weak operational performance — operating margin is only {value}%.",
    },
    "roe": {
        "pro": "Excellent shareholder value creation with ROE at {value}%.",
        "con": "Poor return for shareholders — ROE is only {value}%.",
    },
    "cash_flow_growth": {
        "pro": "Healthy cash flow growth ({value}%).",
        "con": "Weak cash flow growth at {value}%.",
    },
    "debt_ratio": {
        "pro": "Company is almost debt-free (debt ratio at {value}).",
        "con": "Debt levels are high with debt ratio at {value}.",
    },
}

def _is_number(x) -> bool:
    try:
        return x is not None and not math.isnan(float(x))
    except Exception:
        return False

def classify_metric(value: float, threshold: float = DEFAULT_THRESHOLD) -> Optional[str]:
    """
    Return "pro" if value > threshold, "con" if value < threshold, else None.
    Assumes value is a ratio (e.g. 0.2 for 20%) for percentage-like metrics.
    """
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    try:
        v = float(value)
    except Exception:
        return None

    if v > threshold:
        return "pro"
    if v < threshold:
        return "con"
    return None

def format_value_for_template(value: float) -> str:
    """
    Format numbers: if value looks like a ratio (< 2), show as percentage with 1-2 decimals.
    Otherwise print as-is (e.g., ratios like 0.5 -> 50.0%).
    """
    try:
        v = float(value)
    except Exception:
        return str(value)
    if abs(v) < 2:  # probably a ratio like 0.12
        return f"{round(v * 100, 2)}"
    return f"{round(v, 2)}"

def generate_insight(metric_name: str, value: float, classification: str) -> str:
    """Render a human-readable insight using templates; fallback if metric unknown."""
    if metric_name in INSIGHT_TEMPLATES and classification in INSIGHT_TEMPLATES[metric_name]:
        tmpl = INSIGHT_TEMPLATES[metric_name][classification]
        return tmpl.format(value=format_value_for_template(value))
    # fallback generic message
    pct = format_value_for_template(value)
    if classification == "pro":
        return f"{metric_name} is strong ({pct})."
    return f"{metric_name} is weak ({pct})."

def analyze_company(company_id: str, metrics: Dict[str, Any], threshold: float = DEFAULT_THRESHOLD) -> Dict[str, Any]:
    """
    Analyze a company's numeric metrics (dict). Returns:
    {
      "company_id": "...",
      "top_pros": [ {metric, value, insight}, ... up to 3 ],
      "top_cons": [ ... up to 3 ]
    }
    Metrics input expects floats/ratios (e.g., 0.2 for 20%).
    """
    pros: List[Dict[str, Any]] = []
    cons: List[Dict[str, Any]] = []

    for metric, raw_value in (metrics or {}).items():
        if not _is_number(raw_value):
            continue
        value = float(raw_value)
        cls = classify_metric(value, threshold=threshold)
        if cls is None:
            continue
        insight = generate_insight(metric, value, cls)
        entry = {"metric": metric, "value": value, "insight": insight}
        if cls == "pro":
            pros.append(entry)
        else:
            cons.append(entry)

    # Sort pros by highest positive strength (largest value first)
    pros_sorted = sorted(pros, key=lambda x: x["value"], reverse=True)[:3]
    # Sort cons by worst values first. For cons lower value is worse if metric positive;
    # but some metrics might be negative (like negative growth) - sort by value ascending.
    cons_sorted = sorted(cons, key=lambda x: x["value"])[:3]

    return {
        "company_id": company_id,
        "top_pros": pros_sorted,
        "top_cons": cons_sorted
    }
