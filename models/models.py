from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class MCQ(BaseModel):
    question: str
    options: List[str]
    answer: str

class MCQDocument(BaseModel):
    file_id: str
    mcqs: List[MCQ]