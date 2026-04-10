from pydantic import BaseModel
from typing import List

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    category: str
    answer: str
    confidence: float
    steps: List[str]
    recommendations: List[str]