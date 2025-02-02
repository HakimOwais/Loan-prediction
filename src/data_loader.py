from components import vector_store
import json
from langchain_core.documents import Document
from uuid import uuid4

# Loading and ingesting data in mongodb vector store

# Load the card data from the JSON file
with open("card_data.json", "r") as file:
    card_data = json.load(file)

# Convert each card into a LangChain Document
documents = []
for card in card_data:
    doc = Document(
        page_content=card["aboutCard"],  # Text content for embedding
        metadata={
            "card_id": str(uuid4()).lower(),  # Unique ID for tracking
            "cardName": card["cardName"].lower(),
            "type": card["type"].lower(),
            "category": card["category"].lower(),
            "benefits": card["benefits"]
        }
    )
    documents.append(doc)

# Add documents to MongoDB Atlas Vector Store
vector_store.add_documents(documents)

# Print verification
for doc in documents:
    print(f"Document added - cardName: {doc.metadata.get('cardName')}, aboutCard: {doc.page_content}")

print(f"Successfully ingested {len(documents)} cards into MongoDB Atlas Vector Store.")


