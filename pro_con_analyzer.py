def explain(metric, value):
    return f"{metric.replace('_', ' ').title()} is at {value}%."

def analyze_pros_cons(cleaned_data):
    pros = []
    cons = []

    # Flatten all numbers into one dictionary
    flat = {}

    for section, data in cleaned_data.items():
        for key, val in data.items():
            if isinstance(val, (int, float)):
                flat[key] = val

    # Apply rules
    for metric, value in flat.items():

        # PRO → value > 10%
        if value > 10:
            pros.append({
                "metric": metric,
                "value": value,
                "explanation": explain(metric, value)
            })

        # CON → value < 10%
        elif value < 10:
            cons.append({
                "metric": metric,
                "value": value,
                "explanation": explain(metric, value)
            })

    # Pick top 3 highest pros → sort desc
    top_pros = sorted(pros, key=lambda x: x["value"], reverse=True)[:3]

    # Pick top 3 worst cons → sort asc
    top_cons = sorted(cons, key=lambda x: x["value"])[:3]

    return {
        "top_pros": top_pros,
        "top_cons": top_cons
    }
