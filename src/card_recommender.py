from components import vector_store

def recommend_card_based_on_user_input(user_input: dict, category: str):
    # Convert user input into a query
    query = f"User Category: {category}, Preferences: {user_input}"

    # Define filter conditions based on category
    filter_condition = {"category": category}  

    # Fetch the most relevant cards
    results = vector_store.similarity_search(query, k=3, pre_filter=filter_condition)

    return results

# Example user input for a "Salaried" person
input_test = {
  "cashback_on_bills_shopping": "yes",
  "travel_benefits": "no",
  "low_annual_fee": "yes",
  "high_reward_points": "yes"
}

# Recommend a card for a salaried user
results = recommend_card_based_on_user_input(input_test, "salaried")

# Print the recommendations
for res in results:
    print(f"* {res.page_content} [{res.metadata}]")

