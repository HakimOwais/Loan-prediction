from src.components import vector_store_savingplan


query = "recommend me some svaing plans for very medium withrawal flexibility, the minimum amount I can deposit is  2500, and for monthly  down paymet i can deposit 100 "
filter_condition = {"category": {"$eq": "salaried"}}
result = vector_store_savingplan.similarity_search(query, k=2, pre_filter=filter_condition)
print(result)

def recommend_saving_plans(category, withdrawal_flexibility, minimum_monthly_payment):
    query = """Recommend me some saving plans based on the information below:

    Information: 
    I can do the minimum monthly monthly payment : {minimum_monthly_payment},
    I need {withdrawal_flexibility} withdrawal flexibility
    """
    filter_condition = {"category": {"$eq": category}}
    result = vector_store_savingplan.similarity_search(query, k=2, pre_filter=filter_condition)
    return result

