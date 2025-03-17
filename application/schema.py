from pydantic import BaseModel, EmailStr, root_validator
from typing import List
from typing import Dict, Literal, Optional
from datetime import date

# Define input model for card recommendation
class RecommendationRequest(BaseModel):
    category: str
    answers: Dict[str, str]

class PersonalizedChat(BaseModel):
    email: str
    query: str

class AccountDetails(BaseModel):
    account_type: Literal["Saving Account", "Current Account", "Salary Account", "Student Account", "Business Account"]
    category: Literal["savings", "current", "salaried", "student", "business"]
    employer_name: Optional[str] = None  # Only required for salaried accounts

    @classmethod
    def validate_employer_name(cls, values):
        if values.get("category") == "salaried" and not values.get("employer_name"):
            raise ValueError("Employer Name is required for Salary Account")
        return values

class CustomerDetails(AccountDetails):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    dob: str  # Keeping as string since format is "DD-MM-YYYY"
    gender: str
    nationality: str
    government_id: str
    password: str
    residential_address: str
    mailing_address: str
    city: str = ""
    state: str = ""
    zip: str = ""
    ssn_tin: str

class LoginRequest(BaseModel):
    phone: str
    password: str

    



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