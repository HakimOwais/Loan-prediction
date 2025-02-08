from components import vector_store, vector_store_savingplan
import json
from langchain_core.documents import Document
from uuid import uuid4

# Loading and ingesting data in mongodb vector store
def card_loader():
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

# saving plan Loader
def saving_plan_loader():
    # Load the card data from the JSON file
    with open("saving_plans.json", "r") as file:
        saving_plans = json.load(file)
    documents = []

    for saving_plan in saving_plans:
        doc = Document(
            page_content=saving_plan["aboutsavingPlan"],  # Text content for embedding
            metadata={
            "plan_id": saving_plan["plan_id"],  # Unique Plan ID
            "name": saving_plan["name"],
            "category": saving_plan["category"],
            "interest_rate": saving_plan["interest_rate"],
            "minimum_balance": saving_plan["minimum_balance"],
            "withdrawal_flexibility": saving_plan["withdrawal_flexibility"],
            "minimum_monthly_payment": saving_plan["minimum_monthly_payment"],
            "target_audience": saving_plan["target_audience"],
            "features": saving_plan["features"],
            "minimum_annual_income": saving_plan["minimum_annual_income"]
        }
    )
        documents.append(doc)

    # Add documents to MongoDB Atlas Vector Store
    vector_store_savingplan.add_documents(documents)
    print(f"Successfully ingested {len(documents)} saving plans into MongoDB Atlas Vector Store.")

# card_loader()
# saving_plan_loader()