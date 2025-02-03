from src.components import vector_store

category_questions = {
    "student": [
        "Do you frequently spend on food, education, or entertainment? (Yes/No)",
        "Do you shop online or dine out frequently? (Yes/No)",
        "What type of benefits do you prefer? (Dropdown: Cashback, Rewards, Discounts)",
        "Do you travel internationally? (Yes/No)"
    ],
    "salaried": [
        "Do you want cashback on bill payments & online shopping? (Yes/No)",
        "Do you prefer travel benefits like lounge access & air miles? (Yes/No)",
        "Are you looking for a low annual fee card? (Yes/No)",
        "Do you need a credit card with high reward points? (Yes/No)"
    ],
    "business": [
        "Do you frequently make high-value transactions? (Yes/No)",
        "Do you want a corporate credit card for employees? (Yes/No)",
        "Do you prefer business travel perks? (Dropdown: Lounge Access, Flight Upgrades, None)",
        "Do you need higher credit limits? (Yes/No)"
    ]
}


def recommend_card_based_on_user_input(user_input: dict, category: str):
    # Validate category
    if category.lower() not in category_questions:
        raise ValueError("Invalid category. Choose from: student, salaried, business")

    # Get relevant questions for the category
    questions = category_questions[category.lower()]

    # Format the user input into a structured query
    query = f"User Category: {category}, Preferences: "
    for i, question in enumerate(questions):
        answer = user_input.get(f"q{i+1}", "No answer provided")  # Handling missing answers
        query += f"{question} -> {answer}. "

    # Define MongoDB filter
    filter_condition = {"category": category.lower()}

    # Retrieve recommended cards
    results = vector_store.similarity_search(query, k=3, pre_filter=filter_condition)

    return results
