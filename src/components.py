from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain import hub
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Setting up langsmith for tracing

LANGSMITH_TRACING=True
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY=os.environ.get("LANGSMITH_API_KEY")
LANGSMITH_PROJECT="pr-ordinary-mining-51"
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")

# Setting up Chat Model
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Setting up embedding model
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# Setting up vector Store (Giving MongoDB a try)
# initialize MongoDB python client
client = MongoClient(os.environ.get("MONGO_URI"))
DB_NAME = "card_recommendation"
COLLECTION_NAME = "card_details_bank_name"
MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]
ATLAS_VECTOR_SEARCH_INDEX_NAME = "card_vector_index"

vector_store = MongoDBAtlasVectorSearch(
    embedding=embeddings,
    collection=MONGODB_COLLECTION,
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    relevance_score_fn="cosine",
)

# DB setup for transaction collection
TRANSACTION_COLLECTION_NAME = "transactions"
TRANSACTION_COLLECTION = client[DB_NAME][TRANSACTION_COLLECTION_NAME]

# SAVING PLAN SETUP
SAVINGPLAN_COLLECTION_NAME = "saving_plans"
SAVINGPLAN_COLLECTION = client[DB_NAME][SAVINGPLAN_COLLECTION_NAME]
ATLAS_VECTOR_SEARCH_INDEX_NAME = "saving_plan_index"
vector_store_savingplan = MongoDBAtlasVectorSearch(
    embedding=embeddings,
    collection=SAVINGPLAN_COLLECTION,
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    relevance_score_fn="cosine",
)

