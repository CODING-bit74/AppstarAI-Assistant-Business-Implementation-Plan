from pymongo import MongoClient
import os

def get_db():
    """Connect to MongoDB container"""
    uri = os.getenv("MONGO_URI", "mongodb://mongo:27017")
    client = MongoClient(uri)
    return client[os.getenv("MONGO_DB", "appstarai_db")]

