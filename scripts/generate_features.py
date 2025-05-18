# scripts/generate_features.py

import pandas as pd
from pymongo import MongoClient
from feature_engineering import generate_indicators

client = MongoClient("mongodb+srv://dseStoc:asdFGH@dsestock.vvlfbrf.mongodb.net/dsestock")
db = client["dsestock"]
raw_collection = db["stocks"]
features_collection = db["processed_features"]

# Load data from MongoDB
df = pd.DataFrame(list(raw_collection.find({}, {"_id": 0})))

# Clean and process
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(by="date").copy()

all_symbols = []

for symbol in df["symbol"].unique():
    print(f"🔍 Processing {symbol}")
    df_symbol = df[df["symbol"] == symbol].copy()
    df_with_features = generate_indicators(df_symbol)
    all_symbols.append(df_with_features)

# Combine and clean
combined = pd.concat(all_symbols, ignore_index=True)
print("Before dropna:", combined.shape)
combined = combined.dropna()
print("After dropna:", combined.shape)

# Save to MongoDB
if not combined.empty:
    features_collection.delete_many({})
    features_collection.insert_many(combined.to_dict("records"))
    print("✅ Features generated and stored in MongoDB.")
else:
    print("⚠️ No valid data to insert into MongoDB.")