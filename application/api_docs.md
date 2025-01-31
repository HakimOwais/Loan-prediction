```markdown
# Loan Prediction API Documentation

## Overview
This API provides loan eligibility predictions based on user input data. It is built using FastAPI and leverages a machine learning model for classification.

## Endpoints

### **1. Root Endpoint**
**URL**: `/`

**Method**: `GET`

**Description**: Returns a welcome message indicating that the API is running.

**Response Example**:
```json
{
  "message": "Welcome to Loan Prediction App"
}
```

### **2. Loan Prediction Endpoint**
**URL**: `/predict`

**Method**: `POST`

**Description**: Predicts loan eligibility based on input features.

**Request Body (JSON)**:
```json
{
  "Dependents": 2,
  "Education": "Graduate",
  "Self_Employed": "No",
  "TotalIncome": 9600000,
  "LoanAmount": 500000,
  "Loan_Amount_Term": 15,
  "Credit_History": 1,
  "Residential_Assets_Value": 3000000,
  "Commercial_Assets_Value": 500000,
  "Luxury_Assets_Value": 200000,
  "Bank_Asset_Value": 1000000
}
```

**Response Example**:
```json
{
  "Status of Loan Application": "Eligible"
}
```

## Input Parameters
Each request should contain the following fields:
- `Dependents` (int): Number of dependents.
- `Education` (str): Educational qualification (e.g., "Graduate" or "Non Graduate").
- `Self_Employed` (str): Employment status ("Yes" or "No").
- `TotalIncome` (int): Annual income.
- `LoanAmount` (int): Loan amount requested.
- `Loan_Amount_Term` (int): Loan duration in years.
- `Credit_History` (int): Credit score (cibil score).
- `Residential_Assets_Value` (int): Value of residential assets.
- `Commercial_Assets_Value` (int): Value of commercial assets.
- `Luxury_Assets_Value` (int): Value of luxury assets.
- `Bank_Asset_Value` (int): Value of bank assets.

## Response Interpretation
- **"Eligible"**: The applicant qualifies for the loan.
- **"Not Eligible"**: The applicant does not qualify for the loan.


## Usage
The API can be tested using tools like **Postman**, **cURL**, or **FastAPI's interactive Swagger UI** available at `/docs`.

