# ingestion.py
import json
from pymongo import MongoClient
from langchain.schema import Document
import os
import json
import time
import openai
from pymongo import MongoClient
import sys
from pathlib import Path

# # Adding the below path to avoid module not found error
PACKAGE_ROOT = Path(os.path.abspath(os.path.dirname(__file__))).parent
sys.path.append(str(PACKAGE_ROOT))
from src.components import client, llm, embeddings, TRANSACTION_COLLECTION

# Import the MongoDB Atlas Vector Search store and OpenAIEmbeddings.
from langchain_openai import OpenAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient

from dotenv import load_dotenv

# --- Connect to MongoDB ---
ATLAS_VECTOR_SEARCH_INDEX_NAME = "personal_chat_transaction"

# Create the vector store instance fro transactions.
vector_store_transactions = MongoDBAtlasVectorSearch(
    embedding=embeddings,
    collection=TRANSACTION_COLLECTION,
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    relevance_score_fn="cosine",  # or another similarity function as needed
)

# --- Load and convert the JSON data to Documents ---
with open("chatbot/user.json", "r") as file:
    user_data = json.load(file)


def ingest_user_transaction(user_data):
    documents = []

    for user in user_data:
        transactions_str = json.dumps(user["transactions"])  # Convert list to JSON string

        # Document 1: Embedding for user details
        user_doc = Document(    
            page_content=transactions_str,  
            metadata={
                "user_id": user['_id'],
                "name": user['name'],
                "email": user['email'],
                "password": user['password'],  # Password included
            }
        )
        documents.append(user_doc)

    # --- Add Documents to MongoDB Atlas Vector Store ---
    vector_store_transactions.add_documents(documents)

    # --- Verification output ---
    for doc in documents:
        print(f"Document added - Content: {doc.page_content}")
    print(f"Successfully ingested {len(documents)} user embeddings into MongoDB Atlas Vector Store.")

if __name__ == "__main__":
    ingest_user_transaction(user_data)