from pydantic import BaseModel
from typing import List
from typing import Dict

# Define input model for card recommendation
class RecommendationRequest(BaseModel):
    category: str
    answers: Dict[str, str]