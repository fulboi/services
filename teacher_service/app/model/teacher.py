from pydantic import BaseModel, ConfigDict
from typing import Optional


class Student(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int]
    name: str
    current_question: int
    points: int

class Question(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int]
    question_text: str
    question_answer: int