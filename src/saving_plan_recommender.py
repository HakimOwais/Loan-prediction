# # Adding the below path to avoid module not found error
import os
import sys
from pathlib import Path
PACKAGE_ROOT = Path(os.path.abspath(os.path.dirname(__file__))).parent
sys.path.append(str(PACKAGE_ROOT))
from pymongo import MongoClient
from src.components import vector_store_savingplan, SAVINGPLAN_COLLECTION
from chatbot.chain_setup import answer_question_from_context


# query = "recommend me some svaing plans for very medium withrawal flexibility, the minimum amount I can deposit is  2500, and for monthly  down paymet i can deposit 100 "
# filter_condition = {"category": {"$eq": "salaried"}}
# result = vector_store_savingplan.similarity_search(query, k=2, pre_filter=filter_condition)
# print(result)

def recommend_saving_plans(category,  maximum_monthly_payment, maximum_balance, annual_income,  k=5):

    query = f"""
    I am looking for a savings plan that fits within my financial limits.

    Requirements:
    - My maximum initial deposit is {maximum_balance}.
    - My maximum monthly contribution is {maximum_monthly_payment}.
    - The plan should be suitable for someone in the {category} category.

    Recommend only plans that match these criteria.
    """

    # Pre-filter condition for MongoDB Vector Search
    filter_condition = {
        "category": {"$eq": category},  # Match category exactly
        # "withdrawal_flexibility": {"$eq": withdrawal_flexibility},  # Match withdrawal flexibility exactly
        "minimum_balance": {"$lte": maximum_balance},  # Ensure minimum balance is within limit
        "minimum_monthly_payment": {"$lte": maximum_monthly_payment},  # Ensure monthly payment is within limit
        "minimum_annual_income" : {"$lte" : annual_income}
    }

    # Perform vector similarity search with strict pre-filters
    results = vector_store_savingplan.similarity_search(query, k=k, pre_filter=filter_condition)

    # Return only metadata (excluding embeddings or extra details)
    return results



def auto_saving_plan_recommender(category, annual_income, transaction_history, k=3):
    # Calculate maximum balance and maximum monthly payment based on annual income
    maximum_balance = annual_income / 6
    maximum_monthly_payment = annual_income / 12
    
    # Get recommended savings plans based on calculated values
    context = recommend_saving_plans(
        category=category,
        maximum_monthly_payment=maximum_monthly_payment,
        maximum_balance=maximum_balance,
        annual_income=annual_income,
        k=k
    )
    
    # Assuming the function `answer_question_from_context` processes the transaction history
    response = answer_question_from_context(
        context=transaction_history,
        question="suggest me where can I save money based on my transaction history"
    )
    
    return context, response

    


# Calclute saving after months
def calculate_savings(plan_id: str, months: int):
    # Fetch the plan details from MongoDB
    plan = SAVINGPLAN_COLLECTION.find_one({"plan_id": plan_id})
    if not plan:
        return {"error": "Plan not found"}

    # Extract required fields
    initial_deposit = plan["minimum_balance"]
    monthly_payment = plan["minimum_monthly_payment"]
    annual_interest_rate = plan["interest_rate"] / 100  # Convert percentage to decimal
    monthly_interest_rate = annual_interest_rate / 12  # Convert annual interest rate to monthly

    # Compute savings using compound interest formula
    if monthly_interest_rate > 0:
        total_savings = (
            initial_deposit * (1 + monthly_interest_rate) ** months +
            monthly_payment * ((1 + monthly_interest_rate) ** months - 1) / monthly_interest_rate
        )
    else:
        total_savings = initial_deposit + (monthly_payment * months)

    return {
        "plan_id": plan_id,
        "months": months,
        "total_savings": round(total_savings, 2)
    }


if __name__ == "__main__":
    # result = calculate_savings("SP016", 12)
    # print(result)
    transaction_history =  [
        { "date": "2025-01-01", "amount": 3500, "description": "Salary deposit" },
        { "date": "2025-01-02", "amount": -80, "description": "Coffee and snack" },
        { "date": "2025-01-03", "amount": -600, "description": "Grocery shopping" },
        { "date": "2025-01-04", "amount": -120, "description": "Online subscription" },
        { "date": "2025-01-05", "amount": -90, "description": "Book purchase" },
        { "date": "2025-01-06", "amount": -200, "description": "Utility bill" },
        { "date": "2025-01-07", "amount": 500, "description": "Freelance payment" },
        { "date": "2025-01-08", "amount": -350, "description": "Restaurant dinner" },
        { "date": "2025-01-09", "amount": -60, "description": "Movie ticket" },
        { "date": "2025-01-10", "amount": -150, "description": "Clothing purchase" },
        { "date": "2025-01-11", "amount": -90, "description": "Grocery shopping" },
        { "date": "2025-01-12", "amount": -60, "description": "Online course" },
        { "date": "2025-01-13", "amount": 1000, "description": "Bonus" },
        { "date": "2025-01-14", "amount": -100, "description": "Gas refill" },
        { "date": "2025-01-15", "amount": -50, "description": "Coffee shop" },
        { "date": "2025-01-16", "amount": -250, "description": "Electronics purchase" },
        { "date": "2025-01-17", "amount": -150, "description": "Dining out" },
        { "date": "2025-01-18", "amount": -40, "description": "Parking fee" },
        { "date": "2025-01-19", "amount": -30, "description": "Snack purchase" },
        { "date": "2025-01-20", "amount": -100, "description": "Grocery shopping" },
        { "date": "2025-01-21", "amount": 3000, "description": "Salary deposit" },
        { "date": "2025-01-22", "amount": -200, "description": "Internet bill" },
        { "date": "2025-01-23", "amount": -80, "description": "Book purchase" },
        { "date": "2025-01-24", "amount": -150, "description": "Restaurant dinner" },
        { "date": "2025-01-25", "amount": -60, "description": "Online shopping" },
        { "date": "2025-01-26", "amount": -40, "description": "Coffee and snack" },
        { "date": "2025-01-27", "amount": -90, "description": "Grocery shopping" },
        { "date": "2025-01-28", "amount": -130, "description": "Clothing purchase" },
        { "date": "2025-01-29", "amount": -100, "description": "Utility bill" },
        { "date": "2025-01-30", "amount": -50, "description": "Movie ticket" }
        ]
    # context, response = auto_saving_plan_recommender(category="salaried", annual_income=150000, transaction_history=transaction_history, k=3)
    # print(context)
    # print("==========RESPONSE===========")
    # print(response)