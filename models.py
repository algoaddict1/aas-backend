import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

db = client["aas_db"] 
stories_collection = db["stories"]
likes_collection = db["likes"]
comments_collection = db["comments"]
tips_collection = db["tips"]
