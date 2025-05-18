# scripts/generate_signals.py

import pandas as pd
import joblib
from pymongo import MongoClient
import os

# Load model and features
model = joblib.load("models/ai_sinal_model.pkl")
features = joblib.load("models/features.pkl")

# Load data
client = MongoClient("mongodb+srv://dseStoc:asdFGH@dsestock.vvlfbrf.mongodb.net/dsestock")
db = client["dsestock"]
collection = db["processed_features"]
df = pd.DataFrame(collection.find({}, {"_id": 0}))

# Predict per symbol
all_signals = []

for symbol in df["symbol"].unique():
    df_symbol = df[df["symbol"] == symbol].copy()
    df_symbol["predicted_trend"] = model.predict(df_symbol[features])
    df_symbol["signal"] = df_symbol["predicted_trend"].map({1: "buy", 0: "sell"})
    all_signals.append(df_symbol)

# Save to CSV
os.makedirs("signals", exist_ok=True)
for df_symbol in all_signals:
    symbol = df_symbol.iloc[0]["symbol"]
    df_symbol.to_csv(f"signals/{symbol}_signals.csv", index=False)
    print(f"✅ Saved signals for {symbol}")