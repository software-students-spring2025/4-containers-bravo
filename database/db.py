
import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# Create the MongoClient using the provided URI.
client = MongoClient(MONGO_URI)


db = client['emotion_detection']



