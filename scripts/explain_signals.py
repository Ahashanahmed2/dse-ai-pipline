# scripts/explain_signals.py

import shap
import pandas as pd
import joblib
import os

# Load model and features
model = joblib.load("models/ai_sinal_model.pkl")
X = pd.read_csv("data/raw_data.csv")
X = X.dropna(subset=joblib.load("models/features.pkl"))

# SHAP Explainer
explainer = shap.Explainer(model, X[features])
shap_values = explainer(X[features])

# Build explanations
explanations = []
for i in range(len(X)):
    explanation = dict(zip(features, shap_values[i].values))
    explanations.append({
        "symbol": X.iloc[i]["symbol"],
        "date": str(X.iloc[i]["date"]),
        "prediction": int(model.predict([X.iloc[i][features]])),
        **explanation
    })

# Save to CSV
explanation_df = pd.DataFrame(explanations)
output_dir = "explainability_reports"
os.makedirs(output_dir, exist_ok=True)
explanation_df.to_csv(f"{output_dir}/shap_explanations.csv", index=False)
print("✅ SHAP explanations saved.")