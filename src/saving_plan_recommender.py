from pymongo import MongoClient
from src.components import vector_store_savingplan, SAVINGPLAN_COLLECTION


query = "recommend me some svaing plans for very medium withrawal flexibility, the minimum amount I can deposit is  2500, and for monthly  down paymet i can deposit 100 "
filter_condition = {"category": {"$eq": "salaried"}}
result = vector_store_savingplan.similarity_search(query, k=2, pre_filter=filter_condition)
print(result)

def recommend_saving_plans(category, withdrawal_flexibility, maximum_monthly_payment, maximum_balance):
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
        "minimum_monthly_payment": {"$lte": maximum_monthly_payment}  # Ensure monthly payment is within limit
    }

    # Perform vector similarity search with strict pre-filters
    results = vector_store_savingplan.similarity_search(query, k=5, pre_filter=filter_condition)

    # Return only metadata (excluding embeddings or extra details)
    return results


# Calclute saving after months

def calculate_savings(plan_id: str, months: int):
    # Fetch the plan details from MongoDB
    plan = SAVINGPLAN_COLLECTION.find_one({"plan_id": plan_id})
    if not plan:
        return {"error": "Plan not found"}

    # Extract required fields
    initial_deposit = plan["minimum_balance"]
    monthly_payment = plan["minimum_monthly_payment"]
    monthly_interest_rate = plan["interest_rate"] / 100  # Convert percentage to decimal

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


# result = calculate_savings("SP016", 12)
# print(result)
