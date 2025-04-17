# dashboard.py

import streamlit as st
import numpy as np
import pandas as pd
import joblib
import shap
import random
import matplotlib.pyplot as plt

# Load SHAP and sample data
shap_values = np.load("shap_values.npy", allow_pickle=True)
malicious_indices = joblib.load("malicious_indices.pkl")
X_sample = joblib.load("X_sample.pkl")
feature_info = pd.read_csv("session_dataset_feature_explanations.csv")
feature_info.set_index("feature_name", inplace=True)

# Session index state
if "idx" not in st.session_state:
    st.session_state.idx = random.choice(malicious_indices)

idx = st.session_state.idx

# Calculate SHAP explanation for current session
base_value = np.mean(shap_values[1][idx])
explanation = shap.Explanation(
    values=shap_values[1][idx],
    base_values=base_value,
    data=X_sample.iloc[idx],
    feature_names=X_sample.columns
)

# Display session ID
st.markdown(f"### 🆔 Session ID: `{idx}`")

# Full-width SHAP plot at the top
st.markdown("### 📊 SHAP-based Feature Attribution")
fig, ax = plt.subplots()
shap.plots.waterfall(explanation, max_display=10, show=False)
plt.tight_layout()
st.pyplot(fig)

# Stacked interpretation cards below
st.markdown("### 🧠 Key Feature Interpretations and Security Recommendations")
top_indices = np.argsort(-np.abs(shap_values[1][idx]))[:3]  # Show top 3 features

for i in top_indices:
    fname = X_sample.columns[i]
    if fname in feature_info.index:
        row = feature_info.loc[fname]
        with st.container():
            st.markdown(
                f"<div style='border:1px solid #DDD; border-radius:8px; padding:12px; margin-bottom:10px; background-color:#FAFAFA; font-size: 15px; line-height: 1.6em;'>"
                f"<b>🔸 Feature:</b> <code>{fname}</code><br>"
                f"<b>Condition Hint:</b> {row['condition_hint']}<br>"
                f"<b>Interpretation:</b> {row['explanation']}<br>"
                f"<b>Security Recommendation:</b> {row['response_guide']}"
                f"</div>",
                unsafe_allow_html=True
            )
    else:
        st.markdown(f"<div style='border:1px solid #DDD; padding:10px; margin-bottom:10px;'>🔸 Feature: `{fname}` (No interpretation available)</div>", unsafe_allow_html=True)

# Refresh button
if st.button("🔁 Show Next Session"):
    st.session_state.idx = random.choice(malicious_indices)

