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
            {"email": user_details["email"]},
            {"government_id": user_details["government_id"]}
        ]
    })

    if existing_user:
        raise ValueError(
            f"User already exists with email {user_details['email']} or government ID {user_details['government_id']}"
        )

    # Ensure required fields are present
    required_fields = [
        "first_name", "last_name", "dob", "gender", "nationality",
        "residential_address", "mailing_address", "phone", "email",
        "government_id", "ssn_tin", "category", "account_type"
    ]
    
    for field in required_fields:
        if field not in user_details:
            raise ValueError(f"Missing required field: {field}")

    # Ensure account_type and category are valid
    valid_account_types = {
        "Saving Account", "Current Account", "Salary Account", "Student Account", "Business Account"
    }
    valid_categories = {"savings", "current", "salaried", "student", "business"}

    if user_details["account_type"] not in valid_account_types:
        raise ValueError(f"Invalid account type. Choose from: {', '.join(valid_account_types)}")

    if user_details["category"] not in valid_categories:
        raise ValueError(f"Invalid category. Choose from: {', '.join(valid_categories)}")

    # Ensure "Employer Name" is present if account_type is "Salary Account"
    if user_details["account_type"] == "Salary Account" and "employer_name" not in user_details:
        raise ValueError("Employer Name is required for Salary Account")

    # Convert dob to datetime if necessary
    if isinstance(user_details.get("dob"), str):
        try:
            user_details["dob"] = datetime.datetime.strptime(user_details["dob"], "%d-%m-%Y")
        except ValueError:
            raise ValueError("Invalid date format for dob. Use DD-MM-YYYY.")

    # Generate and add a unique 10-digit bank account number
    user_details["bank_account_number"] = generate_unique_account_number()

    # Insert into MongoDB
    inserted_user = MONGODB_USER_COLLECTION.insert_one(user_details)

    return user_details["bank_account_number"]


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
