# Card Recommendation API

## Overview
This API provides category-based questions and recommends suitable credit cards based on user preferences. It supports three user categories: **Student**, **Salaried**, and **Business**.

## Endpoints

### **1. Get Category-Specific Questions**
**URL**: `/get-questions/{category}`

**Method**: `GET`

**Description**: Retrieves a list of relevant questions based on the user's category.

**Path Parameters**:
- `category` (string): User category (one of: `student`, `salaried`, `business`).

**Response Example**:
```json
{
  "category": "student",
  "questions": [
    {"question": "Do you frequently spend on food, education, or entertainment?", "type": "yes_no"},
    {"question": "Do you shop online or dine out frequently?", "type": "yes_no"},
    {"question": "What do you prefer?", "type": "dropdown", "options": ["Cashback", "Rewards", "Discounts"]}
  ]
}
```

**Error Handling**:
- `400 Bad Request`: If the category is invalid.

---

### **2. Recommendation API**
**URL**: `/recommend-card`

**Method**: `POST`

**Description**: Recommends cards based on user responses.

**Request Body (JSON)**:
```json
{
  "category": "salaried",
  "answers": {
    "Do you want cashback on bill payments & online shopping?": "Yes",
    "Do you prefer travel benefits (lounge access, air miles, discounts)?": "No"
  }
}
```

**Response Example**:
```json
{
  "category": "salaried",
  "recommendations": [
    {
      "card_name": "Super Saver Credit Card",
      "about_card": "Earn high cashback on bill payments and shopping."
    },
    {
      "card_name": "Premium Rewards Card",
      "about_card": "High reward points on purchases with minimal fees."
    }
  ]
}
```

**Error Handling**:
- `400 Bad Request`: If the category is invalid.
- `200 OK with message`: If no matching cards are found.

---

## Input Parameters
- `category` (string): User category (`student`, `salaried`, `business`).
- `answers` (dict): Key-value pairs of question responses.

## Response Interpretation
- The response contains a list of recommended credit cards tailored to user preferences.
- If no matching cards are found, a message is returned instead of recommendations.

```

