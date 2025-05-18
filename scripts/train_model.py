# scripts/train_model.py

import pandas as pd
from pymongo import MongoClient
from sklearn.ensemble import RandomForestClassifier
import joblib

# Connect to MongoDB
client = MongoClient("mongodb+srv://dseStoc:asdFGH@dsestock.vvlfbrf.mongodb.net/dsestock")
db = client["dsestock"]
collection = db["processed_features"]

# Load data
df = pd.DataFrame(collection.find({}, {"_id": 0}))

# Define features and target
features = ['rsi', 'macd', 'bb_upper', 'bb_lower', 'obv', 'atr', 'doji', 'engulfing']
df['trend'] = df['change'].apply(lambda x: 1 if x > 0 else 0)

# Drop missing rows
df = df.dropna(subset=features + ['trend'])

# Train model
X = df[features]
y = df['trend']

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model and features
joblib.dump(model, "models/ai_sinal_model.pkl")
joblib.dump(features, "models/features.pkl")

print("✅ Model trained and saved.")