from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
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
import json
from pymongo import MongoClient
from langchain.schema import Document


# # Adding the below path to avoid module not found error
PACKAGE_ROOT = Path(os.path.abspath(os.path.dirname(__file__))).parent
sys.path.append(str(PACKAGE_ROOT))
from application.schema import CustomerDetails, AccountDetails, LoginRequest
from src.user_db import create_new_customer, add_new_account, get_user
from src.database_config import CUSTOMER_COLLECTION

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to allow only specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Adjust this to allow only specific methods
    allow_headers=["*"],  # Adjust this to allow only specific headers
)


@app.get('/')
def index():
    return {'message': 'Welcome to Loan Prediction App'}

@app.get("/check-customer/")
async def check_customer(phone: str):
    """
    Check if a customer exists in the database using their phone number.
    Returns:
    - If the customer exists: message, `ifExists: true`, and user details (excluding sensitive data).
    - If the customer does not exist: message and `ifExists: false`.
    """
    existing_customer = CUSTOMER_COLLECTION.find_one({"phone_number": phone}, {"_id": 0, "password": 0})

    if existing_customer:
        return {
            "message": "Customer exists. You can create a new account.",
            "ifExists": True,
            "user_details": existing_customer  # Returning user details (excluding password)
        }

    return {
        "message": "Customer does not exist. Please proceed with full registration.",
        "ifExists": False
    }


# Create a New Customer (Only for new users)
@app.post("/create-customer/")
async def create_customer(user: CustomerDetails):
    """
    Create a new customer along with their first bank account.
    - If the phone number already exists, reject the request.
    - The function internally handles account number generation.
    """
    existing_customer = CUSTOMER_COLLECTION.find_one({"phone_number": user.phone})

    if existing_customer:
        return {
            "message": "Customer already exists. Please use Login and add new bank account.",
            "ifExists": True
        }

    result = create_new_customer(user.dict())  # Calls function to handle account creation

    return {
        "message": "New customer and account successfully created.",
        "ifExists": False,
        "bank_account_number": result["bank_account_number"]
    }

# Link a New Account to an Existing Customer
@app.post("/link-account/")
async def link_account(phone: str, account: AccountDetails):
    """
    Link a new bank account to an existing customer.
    - Requires only `phone` and `account` details.
    - If the customer does not exist, return an error.
    """
    existing_customer = CUSTOMER_COLLECTION.find_one({"phone_number": phone})

    if not existing_customer:
        return {
            "message": "Customer not found. Please register first using `/create-customer/`.",
            "ifExists": False
        }

    result = add_new_account(existing_customer["_id"], phone, account.dict())  # Calls function to handle account creation

    return {
        "message": "New account successfully linked to existing customer.",
        "ifExists": True,
        "bank_account_number": result["bank_account_number"]
    }

@app.post("/login/")
async def login(request: LoginRequest):
    """
    Authenticate user using phone number and password.
    If successful, return user details and linked bank accounts.
    """
    user_details= get_user(request.phone, request.password)
    return {"message": "Login successful", "user_details" : user_details}
