# Importing Dependencies
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import joblib
import numpy as np
import pandas as pd
import sys
import os
from pathlib import Path
# # Adding the below path to avoid module not found error
PACKAGE_ROOT = Path(os.path.abspath(os.path.dirname(__file__))).parent
sys.path.append(str(PACKAGE_ROOT))

# # Then perform import
from ml_model.configs import config 
from ml_model.processing.data_handling import load_pipeline,load_dataset,separate_data

classification_pipeline = load_pipeline(config.MODEL_NAME)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to allow only specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Adjust this to allow only specific methods
    allow_headers=["*"],  # Adjust this to allow only specific headers
)


#Perform parsing
class LoanPred(BaseModel):
    Dependents: int 
    Education: str 
    Self_Employed: str 
    TotalIncome: int  # 'income_annum'
    LoanAmount: int 
    Loan_Amount_Term: int  # 'loan_term'
    Credit_History: int  # 'cibil_score'
    Residential_Assets_Value: int 
    Commercial_Assets_Value: int
    Luxury_Assets_Value: int 
    Bank_Asset_Value: int 


@app.get('/')
def index():
    return {'message': 'Welcome to Loan Prediction App'}

# defining the function which will make the prediction using the data which the user inputs 
@app.post('/predict')
def predict_loan_status(loan_details: LoanPred):
	data = loan_details.model_dump()
	new_data = {
    'no_of_dependents': data['Dependents'],  # number of people an applicant is financially responsible for, like children or spouses, 
    'education': data['Education'], # e.g Graduate or Non Graduate
    'self_employed': data['Self_Employed'], #Yes or No
    'income_annum': data['TotalIncome'],  # 9600000
    'loan_amount': data['LoanAmount'], 
    'loan_term': data['Loan_Amount_Term'], # years
    'cibil_score': data['Credit_History'], # score
    'residential_assets_value': data['Residential_Assets_Value'],  # market value of the borrower's primary residence
    'commercial_assets_value': data['Commercial_Assets_Value'], # e.g., property, equipment 
    'luxury_assets_value': data['Luxury_Assets_Value'], # cars etc
    'bank_asset_value': data['Bank_Asset_Value']
	}

# Create a DataFrame with a single row from the new_data dictionary
	df = pd.DataFrame([new_data])

	# Making predictions 
	prediction = classification_pipeline.predict(df)

	if prediction[0] == 0:
		pred = 'Not Eligible'
	else:
		pred = 'Eligible'

	return {'Status of Loan Application':pred}

if __name__ == '__main__':
	uvicorn.run(app, host='127.0.0.1', port=8080)