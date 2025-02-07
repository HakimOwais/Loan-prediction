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
    withdrawal_flexibility: str
    maximum_balance: int
    maximum_monthly_payment: int