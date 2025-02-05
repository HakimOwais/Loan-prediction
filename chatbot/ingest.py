# ingestion.py
import json
from pymongo import MongoClient
from langchain.schema import Document
import os
import json
import time
import openai
from pymongo import MongoClient

# Import the MongoDB Atlas Vector Search store and OpenAIEmbeddings.
from langchain_openai import OpenAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient

from dotenv import load_dotenv

# --- Connect to MongoDB ---
client = MongoClient("")
db = client["bank_db"]
users_collection = db["users"]

# --- Set up your MongoDB Atlas Vector Store ---
DB_NAME = "bank_db"
COLLECTION_NAME = "users"  # This collection will store transaction documents
ATLAS_VECTOR_SEARCH_INDEX_NAME = "chat_user_index"
openai.api_key = ""


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

# --- Load and convert the JSON data to Documents ---
with open("chatbot/user.json", "r") as file:
    user_data = json.load(file)

documents = []

for user in user_data:
    transactions_str = json.dumps(user["transactions"])  # Convert list to JSON string

    # Document 1: Embedding for user details
    user_doc = Document(    
        page_content=transactions_str,  
        metadata={
            "_id": user['_id'],
            "name": user['name'],
            "email": user['email'],
            "password": user['password'],  # Password included
        }
    )
    documents.append(user_doc)

# --- Add Documents to MongoDB Atlas Vector Store ---
vector_store.add_documents(documents)

# --- Verification output ---
for doc in documents:
    print(f"Document added - Content: {doc.page_content}")

print(f"Successfully ingested {len(documents)} user embeddings into MongoDB Atlas Vector Store.")
