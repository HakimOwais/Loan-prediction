from src.components import client, TRANSACTION_COLLECTION

DB_NAME = "card_recommendation"
USER_COLLECTIONS = "users"
MONGODB_USER_COLLECTION = client[DB_NAME][USER_COLLECTIONS]

import random
import pymongo
import datetime

def generate_password():
    """Generate a 4-digit password."""
    return str(random.randint(1000, 9999))

def generate_unique_account_number():
    """Generate a unique 10-digit bank account number."""
    while True:
        account_number = str(random.randint(10**9, 10**10 - 1))  # Generate 10-digit number
        if not MONGODB_USER_COLLECTION.find_one({"bank_account_number": account_number}):  # Ensure uniqueness
            return account_number

def authenticate_and_create_transaction(user_id, government_id):
    """
    Ensures a transaction document exists for the user.
    """
    transaction_record = TRANSACTION_COLLECTION.find_one({"user_id": user_id})

    if not transaction_record:
        transaction_data = {
            "user_id": user_id,
            "government_id": government_id,  # Store government ID for reference
            "transactions": []  # Empty list initially
        }
        TRANSACTION_COLLECTION.insert_one(transaction_data)
        return {"message": "Transaction record created", "transaction_id": str(transaction_data["_id"])}
    else:
        return {"message": "Transaction record already exists", "transaction_id": str(transaction_record["_id"])}

def insert_user_details(user_details):
    print(f"Inserting user data into MongoDB: {user_details}")  # Logging

    # Check if user already exists (by email or government ID)
    existing_user = MONGODB_USER_COLLECTION.find_one({
        "$or": [
            {"email_address": user_details["email_address"]},
            {"government_id": user_details["government_id"]}
        ]
    })

    if existing_user:
        raise ValueError(
            f"User already exists with email {user_details['email_address']} or government ID {user_details['government_id']}"
        )

    # Ensure required fields are present
    required_fields = [
        "full_name", "date_of_birth", "gender", "nationality",
        "residential_address", "mailing_address", "phone_number", "email_address",
        "government_id", "ssn_tin", "category"
    ]
    
    for field in required_fields:
        if field not in user_details:
            raise ValueError(f"Missing required field: {field}")
    
    # Ensure category is valid
    valid_categories = {"student", "salaried", "business"}
    if user_details["category"] not in valid_categories:
        raise ValueError("Invalid category. Choose from: student, salaried, business")

    # Convert date_of_birth to datetime if necessary
    if isinstance(user_details.get("date_of_birth"), datetime.date):
        user_details["date_of_birth"] = datetime.datetime.combine(user_details["date_of_birth"], datetime.time())

    # Generate a 4-digit password
    password = generate_password()
    user_details["password"] = password

    # Generate and add a unique 10-digit bank account number
    user_details["bank_account_number"] = generate_unique_account_number()

    # Insert into MongoDB
    inserted_user = MONGODB_USER_COLLECTION.insert_one(user_details)

    # Now create a transaction document for the user
    # authenticate_and_create_transaction(user_details["email_address"], user_details["government_id"])

    return password, user_details["bank_account_number"]


if __name__ == "__main__":
    # Example user data
    user_data = {
        "full_name": "Aarav Sharma",
        "date_of_birth": "1995-08-12",
        "gender": "Male",
        "nationality": "Indian",
        "residential_address": "45, MG Road, Bangalore, Karnataka, India",
        "mailing_address": "P.O. Box 567, Bangalore, Karnataka, India",
        "phone_number": "+91-9876543210",
        "email_address": "aarav.sharma@example.com",
        "government_id": "AID1234567",
        "ssn_tin": "PANX1234A",
        "category": "student"
    }

    # Call the function to insert user details into MongoDB
    password, bank_account_number = insert_user_details(user_data)

    # Output the generated password (if you want to confirm it)
    print(f"Generated password: {password}")
