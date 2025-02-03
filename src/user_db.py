from src.components import client

DB_NAME = "card_recommendation"
USER_COLLECTIONS = "users"
MONGODB_USER_COLLECTION = client[DB_NAME][USER_COLLECTIONS]

import random
import pymongo

def generate_password():
    return str(random.randint(1000, 9999))

from pymongo import MongoClient
import os

import datetime

# def insert_user_details(user_details):
#     print(f"Inserting user data into MongoDB: {user_details}")  # Add logging here
    
#     required_fields = [
#         "full_name", "date_of_birth", "gender", "nationality",
#         "residential_address", "mailing_address", "phone_number", "email_address",
#         "government_id", "ssn_tin", "category"
#     ]
    
#     # Ensure required fields are present
#     for field in required_fields:
#         if field not in user_details:
#             raise ValueError(f"Missing required field: {field}")
    
#     # Ensure category is valid
#     valid_categories = {"student", "salaried", "business"}
#     if user_details["category"] not in valid_categories:
#         raise ValueError("Invalid category. Choose from: student, salaried, business")
    
#     # Convert date_of_birth to datetime if it's a datetime.date object
#     if isinstance(user_details.get("date_of_birth"), datetime.date):
#         user_details["date_of_birth"] = datetime.datetime.combine(user_details["date_of_birth"], datetime.time())

#     # Generate a 4-digit password
#     password = generate_password()
#     user_details["password"] = password
    
#     # Insert into MongoDB
#     try:
#         MONGODB_USER_COLLECTION.insert_one(user_details)
#     except Exception as e:
#         print(f"Error while inserting user into MongoDB: {str(e)}")
#         raise
    
#     return password

def generate_unique_account_number():
    """Generate a unique 10-digit bank account number."""
    while True:
        account_number = str(random.randint(10**9, 10**10 - 1))  # Generate 10-digit number
        if not MONGODB_USER_COLLECTION.find_one({"bank_account_number": account_number}):  # Ensure uniqueness
            return account_number

def insert_user_details(user_details):
    print(f"Inserting user data into MongoDB: {user_details}")  # Logging

    required_fields = [
        "full_name", "date_of_birth", "gender", "nationality",
        "residential_address", "mailing_address", "phone_number", "email_address",
        "government_id", "ssn_tin", "category"
    ]
    
    # Ensure required fields are present
    for field in required_fields:
        if field not in user_details:
            raise ValueError(f"Missing required field: {field}")
    
    # Ensure category is valid
    valid_categories = {"student", "salaried", "business"}
    if user_details["category"] not in valid_categories:
        raise ValueError("Invalid category. Choose from: student, salaried, business")
    
    # Convert date_of_birth to datetime if it's a datetime.date object
    if isinstance(user_details.get("date_of_birth"), datetime.date):
        user_details["date_of_birth"] = datetime.datetime.combine(user_details["date_of_birth"], datetime.time())

    # Generate a 4-digit password
    password = generate_password()
    user_details["password"] = password

    # Generate and add a unique 10-digit bank account number
    user_details["bank_account_number"] = generate_unique_account_number()

    # Insert into MongoDB
    try:
        MONGODB_USER_COLLECTION.insert_one(user_details)
    except Exception as e:
        print(f"Error while inserting user into MongoDB: {str(e)}")
        raise
    
    return password, user_details["bank_account_number"]

if __name__ == "__main__":
    # Example user data
    user_data = {
        "full_name": "John Doe",
        "date_of_birth": "1990-01-01",
        "gender": "Male",
        "nationality": "American",
        "residential_address": "123 Main St, Springfield, IL",
        "mailing_address": "123 Main St, Springfield, IL",
        "phone_number": "555-1234",
        "email_address": "john.doe@example.com",
        "government_id": "A1234567",
        "ssn_tin": "123-45-6789",
        "category": "student"
    }

    # Call the function to insert user details into the MongoDB collection
    password = insert_user_details(None, user_data)

    # Output the generated password (if you want to confirm it)
    print(f"Generated password: {password}")
