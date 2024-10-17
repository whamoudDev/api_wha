from fastapi import APIRouter, Depends, HTTPException # type: ignore
from db import get_db
from quizzes import models
from quizzes.schemas import Quiz, QuizInput
from sqlalchemy.orm import Session

quizzes_router = APIRouter()

@quizzes_router.get("/hi/{name}")
def say_hi(name: str) -> str:
    return f"Hi {name}!"

fake_quizzes: list[Quiz] = [
    Quiz(id= 1, title="Question 1", tags=["str1","str2"]),
    Quiz(id= 2, title="Question 2", tags=["str11","str22"]),
    Quiz(id= 3, title="Question 3", tags=["str111","str222"]),
]

def get_quiz_by_id(id : int) -> Quiz | None:
    for quiz in fake_quizzes:
        if quiz.id == id:
            return quiz
    return None

@quizzes_router.get("/quizzes")
def read_quizzes(db: Session= Depends(get_db)) -> list[Quiz]:
    return db.query(models.Quizz).all()

@quizzes_router.get("/quiz/{id}")
def read_quiz(id : int) -> Quiz:
    quiz = get_quiz_by_id(id)
    if quiz is None:
        raise HTTPException(404, "Quiz not found")
    return quiz

@quizzes_router.post("/add")
def add_quizzes(quiz_input: QuizInput, db: Session= Depends(get_db)) -> Quiz:

    created_quiz = models.Quizz(title=quiz_input.title, tags=quiz_input.tags)
    db.add(created_quiz)
    db.commit()
    db.refresh(created_quiz)
    
    return created_quiz

@quizzes_router.patch("/edit/{id}")
def update_quiz(id : int, input : QuizInput) -> Quiz :
    for quiz in fake_quizzes:
        if quiz.id == id:
            quiz.title = input.title
            quiz.tags = input.tags
            return quiz
    raise HTTPException(404, "Quiz not found")

@quizzes_router.delete("/delete/{id}")
def delete_quiz(id :int) -> str:
    for quiz in fake_quizzes:
        if quiz.id == id:
            fake_quizzes.remove(quiz)
            return "Quiz Supprimé"
    raise HTTPException(404, "Quiz not found")