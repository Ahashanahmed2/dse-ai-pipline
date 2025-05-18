from pymongo import MongoClient
import pandas as pd

from dotenv import load_dotenv # type: ignore
import os
load_dotenv()
mongo_uri = "mongodb+srv://dseStoc:asdFGH@dsestock.vvlfbrf.mongodb.net/?retryWrites=true&w=majority&appName=dseStock"

def fetch_data():
    print(mongo_uri)
    client = MongoClient(mongo_uri)

    coll = client["dsestock"]["stocks"]

    docs = list(coll.find({}, {"_id": 0}))
   
    df = pd.DataFrame(docs)
    df.to_csv("data/raw_data.csv", index=False)


if __name__ == "__main__":
    fetch_data()
