from src.components import vector_store_savingplan


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
