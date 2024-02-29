import os
from dotenv import load_dotenv
from pymongo import MongoClient, server_api

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
MONGO_CLIENT_URI = os.getenv('MONGO_CLIENT_URI')


def get_mongo_client():
    client = MongoClient(MONGO_CLIENT_URI, server_api=server_api.ServerApi('1'))
    return client
