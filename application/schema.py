from pydantic import BaseModel, EmailStr
from typing import List
from typing import Dict
from datetime import date

# Define input model for card recommendation
class RecommendationRequest(BaseModel):
    category: str
    answers: Dict[str, str]

class PersonalizedChat(BaseModel):
    email: str
    query: str

class UserDetails(BaseModel):
    full_name: str
    date_of_birth: date
    gender: str
    nationality: str
    residential_address: str
    mailing_address: str
    phone_number: str
    email_address: EmailStr
    government_id: str
    ssn_tin: str
    category: str
    
    class Config:
        orm_mode = True

class SavingPlanRequest(BaseModel):
    category: str
    maximum_balance: int
    maximum_monthly_payment: int
    annual_income : int

class SavingsRequest(BaseModel):
    plan_id: str
    months: int

class UserTransaction(BaseModel):
    user_id: str
    name: str
    email: str
    password: str  
    transactions: list
    annual_income: int

class Transaction(BaseModel):
    date: str
    amount: float
    category: str

class AutoSavingPlanRequest(BaseModel):
    category: str
    annual_income: float
    transaction_history: List[Transaction]
    k: int = 3