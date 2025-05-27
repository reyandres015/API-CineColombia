import os
from pymongo import MongoClient

DATABASE_URL = os.getenv("DATABASE_URL")

db_client = MongoClient(DATABASE_URL)
