from pymongo import MongoClient
import os

# Connect to MongoDB
client = MongoClient(os.environ.get("MONGO_URI"))

# Database Name
DB_NAME = "bank-demo"
db = client[DB_NAME]

# Collections
CUSTOMER_COLLECTION_NAME = "customers"
CUSTOMER_COLLECTION = db[CUSTOMER_COLLECTION_NAME]

ACCOUNT_COLLECTION_NAME = "accounts"
ACCOUNT_COLLECTION = db[ACCOUNT_COLLECTION_NAME]

TRANSACTION_COLLECTION_NAME = "transactions"
TRANSACTION_COLLECTION = db[TRANSACTION_COLLECTION_NAME]
