import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables

# Read CSV
df = pd.read_csv('../modelling/modified_dataset.csv')

# MongoDB Connection
uri = os.environ.get('MONGO_CLIENT_URI')  # Set the MONGO_CLIENT_URI environment variable

client = MongoClient(uri)
db = client['predictions']
collection = db['dataset']

# Convert DataFrame to Dictionary and Insert into MongoDB
data = df.to_dict(orient='records')
collection.insert_many(data)

# Fetch and display some documents from the collection
for doc in collection.find().limit(10):  # Adjust the limit as needed
    print(doc)