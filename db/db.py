import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("mongoString"))
db = client["hospital_db"]

users_collection = db["users"]
appointments_collection = db["appointments"]








