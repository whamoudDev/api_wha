from pydantic import BaseModel # type: ignore

class Answer(BaseModel):
    text: str
    is_correct: bool

class Question(BaseModel):
    id: int
    text: str
    answers: list[Answer] = []

class QuestionInput(BaseModel):
    text: str
    answers: list[Answer] = []



