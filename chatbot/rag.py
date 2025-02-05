import os
import json
import time
import openai
from pymongo import MongoClient

# Import the MongoDB Atlas Vector Search store and OpenAIEmbeddings.
from langchain_openai import OpenAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient



# --- Connect to MongoDB ---
# client = MongoClient("")
db = client["bank_db"]
users_collection = db["users"]

# --- Set up your MongoDB Atlas Vector Store ---
DB_NAME = "bank_db"
COLLECTION_NAME = "users"  # This collection will store transaction documents
ATLAS_VECTOR_SEARCH_INDEX_NAME = "chat_user_index"

# Instantiate your embedding model (using OpenAI's embedding model)
embeddings = OpenAIEmbeddings(
                              model="text-embedding-ada-002")

# Initialize the MongoDB client and get the collection
# client = MongoClient(MONGO_URI)
collection = client[DB_NAME][COLLECTION_NAME]

# Create the vector store instance.
vector_store = MongoDBAtlasVectorSearch(
    embedding=embeddings,
    collection=collection,
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    relevance_score_fn="cosine",  # or another similarity function as needed
)

def login():
    email = input("Enter email address: ").strip()
    password = input("Enter password: ").strip()
    
    user = users_collection.find_one({"email": email, "password": password})
    if user:
        print("Login successful!")
        return user["_id"]  # Return user ID for future queries
    else:
        print("Invalid email or password. Try again.")
        return None

