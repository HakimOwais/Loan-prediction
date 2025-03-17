from src.components import client, TRANSACTION_COLLECTION
from src.database_config import ACCOUNT_COLLECTION, CUSTOMER_COLLECTION, TRANSACTION_COLLECTION
from fastapi import HTTPException

DB_NAME = "card_recommendation"
USER_COLLECTIONS = "users"
MONGODB_USER_COLLECTION = client[DB_NAME][USER_COLLECTIONS]

import random
import pymongo
import datetime
from bson import ObjectId

def generate_password():
    """Generate a 4-digit password."""
    return str(random.randint(1000, 9999))

# Function to generate a unique 10-digit bank account number
def generate_unique_account_number():
    while True:
        account_number = str(random.randint(10**9, 10**10 - 1))
        if not ACCOUNT_COLLECTION.find_one({"account_number": account_number}):
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

# Function to create customer and link accounts
def create_new_customer(user_details):
    """ Creates a new customer and account """

    print(f"Inserting new customer into MongoDB: {user_details}")  # Logging

    # Convert dob to datetime
    try:
        user_details["dob"] = datetime.datetime.strptime(user_details["dob"], "%d-%m-%Y")
    except ValueError:
        raise ValueError("Invalid date format for dob. Use DD-MM-YYYY.")

    # Generate bank account number
    bank_account_number = generate_unique_account_number()

    # Prepare first account entry
    account_entry = {
        "account_number": bank_account_number,
        "account_type": user_details["account_type"],
        "category": user_details["category"],
    }
    if user_details["category"] == "salaried":
        account_entry["employer_name"] = user_details["employer_name"]

    # Insert new customer
    new_customer = {
        "first_name": user_details["first_name"],
        "last_name": user_details["last_name"],
        "phone_number": user_details["phone"],
        "email": user_details["email"],
        "dob": user_details["dob"],
        "gender": user_details["gender"],
        "nationality": user_details["nationality"],
        "residential_address": user_details["residential_address"],
        "mailing_address": user_details["mailing_address"],
        "government_id": user_details["government_id"],
        "ssn_tin": user_details["ssn_tin"],
        "password" : user_details["password"],
        "linked_accounts": [account_entry]
    }
    insert_result = CUSTOMER_COLLECTION.insert_one(new_customer)

    # Insert new account
    new_account = {
        "user_id": insert_result.inserted_id,
        "phone_number": user_details["phone"],
        "account_number": bank_account_number,
        "account_type": user_details["account_type"],
        "category": user_details["category"],
        "balance": 0.00,
        "created_at": datetime.datetime.utcnow()
    }
    if user_details["category"] == "salaried":
        new_account["employer_name"] = user_details["employer_name"]

    ACCOUNT_COLLECTION.insert_one(new_account)

    return {"message": "User created successfully", "bank_account_number": bank_account_number}

def add_new_account(user_id, phone, account_details):
    """ Adds a new account to an existing user """

    print(f"Adding new account to existing user {user_id}: {account_details}")  # Logging

    # Generate bank account number
    bank_account_number = generate_unique_account_number()

    # Prepare account entry
    account_entry = {
        "account_number": bank_account_number,
        "account_type": account_details["account_type"],
        "category": account_details["category"]
    }
    if account_details["category"] == "salaried":
        account_entry["employer_name"] = account_details["employer_name"]

    # Add to linked_accounts in customers collection
    CUSTOMER_COLLECTION.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {"linked_accounts": account_entry}}
    )

    # Insert new account in accounts collection
    new_account = {
        "user_id": user_id,
        "phone_number": phone,
        "account_number": bank_account_number,
        "account_type": account_details["account_type"],
        "category": account_details["category"],
        "balance": 0.00,
        "created_at": datetime.datetime.utcnow()
    }
    if account_details["category"] == "salaried":
        new_account["employer_name"] = account_details["employer_name"]

    ACCOUNT_COLLECTION.insert_one(new_account)

    return {"message": "New account linked successfully", "bank_account_number": bank_account_number}

def serialize_mongo_document(doc):
    """Convert MongoDB documents to JSON-serializable format."""
    if not doc:
        return None
    doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
    return doc


def get_user(phone: str, password: str):
    """
    Fetch user details and linked accounts using phone number and password.
    If authentication fails, raise an HTTPException.
    """
    # Find customer by phone number
    customer = CUSTOMER_COLLECTION.find_one({"phone_number": phone})

    if not customer or customer["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid phone number or password")

    # Fetch all linked accounts for the user
    accounts = list(ACCOUNT_COLLECTION.find({"phone_number": phone}, {"_id": 0}))
    print(type(accounts))

    user_details = {
            "first_name": customer["first_name"],
            "last_name": customer["last_name"],
            "email": customer["email"],
            "phone_number": customer["phone_number"],
            "dob": customer["dob"].strftime("%d-%m-%Y"),
            "gender": customer["gender"],
            "nationality": customer["nationality"],
            "residential_address": customer["residential_address"],
            "mailing_address": customer["mailing_address"],
            "government_id": customer["government_id"],
            "ssn_tin": customer["ssn_tin"],
            "linked_accounts" : customer["linked_accounts"]
        }
    return user_details

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

    # # Call the function to insert user details into MongoDB
    # password, bank_account_number = insert_user_details(user_data)

    # Output the generated password (if you want to confirm it)
    # print(f"Generated password: {password}")
