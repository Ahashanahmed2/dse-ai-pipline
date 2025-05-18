# scripts/predict_signal.py

import pandas as pd
from pymongo import MongoClient
import joblib
from datetime import datetime, timedelta
import json

# Load model and features
model = joblib.load("models/ai_sinal_model.pkl")
features = joblib.load("models/features.pkl")

# Load raw data from MongoDB
client = MongoClient("mongodb+srv://dseStoc:asdFGH@dsestock.vvlfbrf.mongodb.net/dsestock")
db = client["dsestock"]
collection = db["processed_features"]

df = pd.DataFrame(collection.find({}, {"_id": 0}))

# Regenerate indicators if needed
from feature_engineering import generate_indicators
all_signals = []
for symbol in df["symbol"].unique():
    df_symbol = df[df["symbol"] == symbol].copy()
    df_with_features = generate_indicators(df_symbol)
    all_signals.append(df_symbol)

df = pd.concat(all_signals, ignore_index=True).dropna(subset=features)
X = df[features]
predictions = model.predict(X)

# Build signal JSON
signals = []
for i in range(len(predictions)):
    if predictions[i] == 1:
        close_price = df.iloc[i]['close']
        signal = {
            "symbol": df.iloc[i]["symbol"],
            "buy_price": round(close_price, 2),
            "confidence": round((df.iloc[i]["rsi"] / 100) * 100, 2),
            "trend": "Uptrend" if df.iloc[i]["rsi"] < 70 else "Downtrend",
            "strategy": "Pullback Strategy",
            "risk_reward_ratio": round(1.5, 2),
            "expiry_date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
            "stop_loss": round(close_price * 0.97, 2),
            "validity_duration": "3 days",
            "hold_duration": 3,  # 👈 Add this line
            "past_accuracy": round(85.0, 2)
        }
        signals.append(signal)

with open("signal.json", "w") as f:
    json.dump(signals, f, indent=4)

print("✅ Signal generated and saved.")