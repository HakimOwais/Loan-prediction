# Importing Dependencies

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import joblib
import numpy as np
import pandas as pd
import sys
import os
from pathlib import Path
from fastapi import Query

import json
from typing import Dict, List


# # Adding the below path to avoid module not found error
PACKAGE_ROOT = Path(os.path.abspath(os.path.dirname(__file__))).parent
sys.path.append(str(PACKAGE_ROOT))
from src.card_recommender import category_questions, recommend_card_based_on_user_input
from src.components import vector_store
from application.schema import RecommendationRequest, UserDetails, PersonalizedChat, SavingPlanRequest
from src.user_db import insert_user_details
from chatbot.rag import qa_transactions_driver
from src.saving_plan_recommender import recommend_saving_plans


# # Then perform import
from ml_model.configs import config 
from ml_model.processing.data_handling import load_pipeline,load_dataset,separate_data

classification_pipeline = load_pipeline(config.MODEL_NAME)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to allow only specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Adjust this to allow only specific methods
    allow_headers=["*"],  # Adjust this to allow only specific headers
)


#Perform parsing
class LoanPred(BaseModel):
    Dependents: int 
    Education: str 
    Self_Employed: str 
    TotalIncome: int  # 'income_annum'
    LoanAmount: int 
    Loan_Amount_Term: int  # 'loan_term'
    Credit_History: int  # 'cibil_score'
    Residential_Assets_Value: int 
    Commercial_Assets_Value: int
    Luxury_Assets_Value: int 
    Bank_Asset_Value: int 


@app.get('/')
def index():
    return {'message': 'Welcome to Loan Prediction App'}

# defining the function which will make the prediction using the data which the user inputs 
@app.post('/predict')
def predict_loan_status(loan_details: LoanPred):
	data = loan_details.model_dump()
	new_data = {
    'no_of_dependents': data['Dependents'],  # number of people an applicant is financially responsible for, like children or spouses, 
    'education': data['Education'], # e.g Graduate or Non Graduate
    'self_employed': data['Self_Employed'], #Yes or No
    'income_annum': data['TotalIncome'],  # 9600000
    'loan_amount': data['LoanAmount'], 
    'loan_term': data['Loan_Amount_Term'], # years
    'cibil_score': data['Credit_History'], # score
    'residential_assets_value': data['Residential_Assets_Value'],  # market value of the borrower's primary residence
    'commercial_assets_value': data['Commercial_Assets_Value'], # e.g., property, equipment 
    'luxury_assets_value': data['Luxury_Assets_Value'], # cars etc
    'bank_asset_value': data['Bank_Asset_Value']
	}

# Create a DataFrame with a single row from the new_data dictionary
	df = pd.DataFrame([new_data])

	# Making predictions 
	prediction = classification_pipeline.predict(df)

	if prediction[0] == 0:
		pred = 'Not Eligible'
	else:
		pred = 'Eligible'

	return {'Status of Loan Application':pred}


# Endpoint to get category-specific questions
@app.get("/get-questions/{category}")
def get_questions(category: str):
    if category.lower() not in category_questions:
        raise HTTPException(status_code=400, detail="Invalid category. Choose from: student, salaried, business")
    return {"category": category, "questions": category_questions[category.lower()]}



# Endpoint to recommend a card
@app.post("/recommend-card")
def recommend_card(request: RecommendationRequest):
    category = request.category.lower()
    user_input = request.answers
    
    if category not in category_questions:
        raise HTTPException(status_code=400, detail="Invalid category")
    # # Convert user input into a query
    # query = f"User Category: {category}, Preferences: {json.dumps(user_input)}"

    # # Define MongoDB filter
    # filter_condition = {"category": category}

    # Fetch recommended cards
    # results = vector_store.similarity_search(query, k=3, pre_filter=filter_condition)
    results = recommend_card_based_on_user_input(user_input, category)

    if not results:
        return {"message": "No matching cards found for your preferences."}
    recommended_cards = [
        {"card_name": res.metadata.get("cardName"), "about_card": res.page_content, "type" : res.metadata.get("type"),"benefits": res.metadata.get("benefits") }
        for res in results
    ]
    return {"category": category, "recommendations": recommended_cards}

@app.post("/personalized_chat")
async def personalised_chat(chat_input : PersonalizedChat):
     try:
          chat_input_data = chat_input.model_dump()

          response = qa_transactions_driver(email=chat_input_data["email"], query=chat_input_data["query"])
          # Return the response (assuming qa_transactions_driver returns a result)
          return {"status": "success", "response": response}
     except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/users/")
async def create_user(user: UserDetails):
    try:
        user_data = user.model_dump()  # Convert Pydantic model to dict (use .dict() for Pydantic v1)

        print(f"Received user data: {user_data}")  # Logging

        # Insert user details into MongoDB
        password, bank_account_number = insert_user_details(user_data)

        return {
            "message": "User created successfully",
            "password": password,
            "bank_account_number": bank_account_number
        }

    except ValueError as e:
        print(f"ValueError: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))  # <-- Now it will show in Swagger docs!

    except Exception as e:
        print(f"Exception: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

from src.components import client

DB_NAME = "card_recommendation"
USER_COLLECTIONS = "users"
MONGODB_USER_COLLECTION = client[DB_NAME][USER_COLLECTIONS]

@app.get("/get_users/")
async def get_user(phone_number: str = Query(...), password: str = Query(...)):
    try:
        # Fetch user from MongoDB using phone number and password
        user = MONGODB_USER_COLLECTION.find_one(
            {"phone_number": phone_number, "password": password}, 
            {"_id": 0}  # Exclude MongoDB's default `_id` field
        )

        if not user:
            raise HTTPException(status_code=404, detail="User not found or incorrect credentials")

        return {"message": "User retrieved successfully", "user": user}

    except Exception as e:
        print(f"Exception: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
# Route for recommendation
@app.post("/recommend_saving_plans", response_model=List[Dict])
async def recommend_saving_plans_route(request: SavingPlanRequest):
    # Call the existing function `recommend_saving_plans` with the provided parameters
    result = recommend_saving_plans(
        category=request.category,
        withdrawal_flexibility=request.withdrawal_flexibility,
        # minimum_balance=request.minimum_balance,
        minimum_monthly_payment=request.minimum_monthly_payment
    )

    # Extract only metadata part from the result
    metadata_result = [doc.metadata for doc in result]

    return metadata_result

if __name__ == '__main__':
	uvicorn.run(app, host='127.0.0.1', port=8080)