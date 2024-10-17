from fastapi import APIRouter, Depends, HTTPException # type: ignore
from db import get_db
from quizzes import models
from quizzes.schemas import Quiz, QuizInput
from sqlalchemy.orm import Session

quizzes_router = APIRouter()

def get_quiz_by_id(id : int, db : Session) -> Quiz | None:
    return db.query(models.Quizz).filter(models.Quizz.id==id).first()

@quizzes_router.get("/quizzes")
def read_quizzes(db: Session= Depends(get_db)) -> list[Quiz]:
    return db.query(models.Quizz).all()

@quizzes_router.get("/quiz/{id}")
def read_quiz(id : int, db: Session= Depends(get_db)) -> Quiz:
    quiz = get_quiz_by_id(id ,db)
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
def update_quiz(id : int, input : QuizInput, db: Session= Depends(get_db)) -> Quiz :
    quiz = get_quiz_by_id(id, db)
    if quiz is None:
        raise HTTPException(404, "Quiz not found")
    quiz.title = input.title
    quiz.tags = input.tags
    db.commit()
    return quiz
    
@quizzes_router.delete("/delete/{id}")
def delete_quiz(id :int, db: Session= Depends(get_db)) -> str:
    quiz = get_quiz_by_id(id, db)
    if quiz is None:
        raise HTTPException(404, "Quiz not found")

    db.delete(quiz)
    db.commit()
    return "Delete Ok"
        