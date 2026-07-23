from pydantic import BaseModel
from typing import List

class QuestionModel(BaseModel):
    question: str
    options: List[str]
    correct_option: str
    explanation: str
    
class StartGameRequest(BaseModel):
    category: str
    difficulty: str = "medium"
    
class SubmitAnswerRequest(BaseModel):
    session_id: str
    selected_option: str
    
class AnswerResponse(BaseModel):
    is_correct: bool
    correct_option: str
    explanation: str
    current_score: int