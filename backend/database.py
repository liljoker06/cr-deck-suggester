from pymongo import MongoClient
import os

def get_database():
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    client = MongoClient(MONGO_URL)
    return client["clash_decks"]
