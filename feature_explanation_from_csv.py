# feature_explanation_generator.py

import pandas as pd

# ✅ Security interpretation rules + generalized fallback templates (ENGLISH)
rules = [
    {"keywords": ["time", "min"], "condition_hint": "If the value is 0 or very small",
     "explanation": "Very short inter-packet times may indicate automated or scripted traffic.",
     "response_guide": "Consider applying detection rules for bots or automated tools."},

    {"keywords": ["tcp", "window", "change"], "condition_hint": "If the value is large",
     "explanation": "Large changes in TCP window size may indicate evasion or scanning behavior.",
     "response_guide": "Apply rules to detect abnormal TCP behaviors."},

    {"keywords": ["ip", "packet", "min"], "condition_hint": "If the value is small",
     "explanation": "A high ratio of short IP packets may indicate C2 (command/control) traffic.",
     "response_guide": "Consider filtering sessions with short, repetitive packets."},

    {"keywords": ["ttl", "var"], "condition_hint": "If the value is high",
     "explanation": "High TTL variance may indicate routing evasion or proxy use.",
     "response_guide": "Enable detection rules based on TTL anomalies."},

    {"keywords": ["payload", "length", "total"], "condition_hint": "If the value is large",
     "explanation": "Abnormally large payloads may indicate data exfiltration or tunneling.",
     "response_guide": "Monitor sessions with high payload volume."},

    {"keywords": ["ratio"], "condition_hint": "If the value is between 0.3 and 0.6",
     "explanation": "Suspicious traffic ratios may imply focused attacks or scanning activity.",
     "response_guide": "Analyze concentrated traffic by IP or port."},

    {"keywords": ["flow", "duration"], "condition_hint": "If the value is high",
     "explanation": "Very long sessions may be indicative of tunneling or evasion channels.",
     "response_guide": "Review policies related to session duration limits."},
]

# 📦 Generalized fallback templates for any feature
fallback_templates = [
    {"pattern": "mean", "condition": "If the mean is high",
     "explanation": "High mean values may suggest excessive or continuous activity.",
     "response": "Check whether the metric consistently exceeds expected thresholds."},

    {"pattern": "std", "condition": "If the standard deviation is large",
     "explanation": "High variability may indicate unstable or erratic behavior in traffic.",
     "response": "Consider rules for detecting irregular patterns."},

    {"pattern": "var", "condition": "If the variance is high",
     "explanation": "High variance could point to inconsistent communication patterns.",
     "response": "Evaluate traffic stability and consider limits or alerts."},

    {"pattern": "total", "condition": "If the total value is high",
     "explanation": "A high total may indicate large data transfers or tunneling.",
     "response": "Monitor for sessions with heavy traffic volume."},

    {"pattern": "max|min", "condition": "If values are extreme",
     "explanation": "Extremely high or low values may indicate outlier or anomalous activity.",
     "response": "Apply threshold-based anomaly detection."},
]

# 🔍 Rule application logic
def apply_rule(feature):
    fname = feature.lower()
    for rule in rules:
        if all(kw in fname for kw in rule["keywords"]):
            return pd.Series({
                "condition_hint": rule["condition_hint"],
                "explanation": rule["explanation"],
                "response_guide": rule["response_guide"]
            })
    for tpl in fallback_templates:
        patterns = tpl["pattern"].split("|")
        if any(p in fname for p in patterns):
            return pd.Series({
                "condition_hint": tpl["condition"],
                "explanation": tpl["explanation"],
                "response_guide": tpl["response"]
            })
    return pd.Series({
        "condition_hint": "(Interpretation may vary depending on value range)",
        "explanation": "This feature does not match specific rules, but may still be relevant based on statistical patterns.",
        "response_guide": "Use traffic distribution analysis to define detection policies."
    })

# 📥 Generate explanations from a dataset CSV
def generate_feature_explanations_from_csv(csv_path):
    df = pd.read_csv(csv_path)
    features = [col for col in df.columns if col.lower() not in ["label", "target"]]
    result = pd.DataFrame({"feature_name": features})
    result[["condition_hint", "explanation", "response_guide"]] = result["feature_name"].apply(apply_rule)
    return result

# ▶️ Example execution
if __name__ == "__main__":
    path = "session_dataset.csv"
    df_result = generate_feature_explanations_from_csv(path)
    output_path = "session_dataset_feature_explanations.csv"
    df_result.to_csv(output_path, index=False)
    print(f"✅ Feature explanations saved to '{output_path}'")

