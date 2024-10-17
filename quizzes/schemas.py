from pydantic import BaseModel # type: ignore
from questions.schemas import Question

class Quiz(BaseModel):
    id: int
    title: str
    tags: list[str] = []
    questions: list[Question]= []

class QuizInput(BaseModel):
    title: str
    tags: list[str] = []
