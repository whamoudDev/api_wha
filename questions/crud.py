from fastapi import APIRouter, Depends, HTTPException # type: ignore
from db import get_db
from questions import models
from questions.schemas import Question, QuestionInput
from quizzes.crud import get_quiz_by_id # type: ignore
from sqlalchemy.orm import Session

questions_router = APIRouter()

# Ancienne version sans db
# @questions_router.post("/quizzes/{quiz_id}/questions")
# def create_question(quiz_id: int, create_question_input: QuestionInput) ->list[Question]:
#     quiz= get_quiz_by_id(quiz_id)
#     if quiz is None:
#         raise HTTPException(404, "Quiz not found")
#
# Notion de décompression de dictionnaire **create_questi.....dict()
#     question = Question(**create_question_input.dict(), id=len(quiz.questions)+1) 
#     quiz.questions.append(question)
#     return quiz.questions

@questions_router.post("/quizzes/{quiz_id}/questions")
def create_question(quiz_id: int, create_question_input: QuestionInput, db: Session= Depends(get_db)) ->Question:
    quiz= get_quiz_by_id(quiz_id, db)
    if quiz is None:
        raise HTTPException(404, "Quiz not found")
    
    created_question = models.Question(
        quiz_id=quiz_id,
        text=create_question_input.text
    )

    db.add(created_question)
    db.commit()
    db.refresh(created_question)

    answers = []
    for answer_input in create_question_input.answers:
        answers.append(
            models.Answer(question_id=create_question.id, **answer_input.dict())
        ) 

    db.add_all(answers)
    db.commit()

    return created_question

@questions_router.get("/quizzes/{quiz_id}/questions")
def get_questions(quiz_id: int, db: Session= Depends(get_db))->list[Question]:
    quiz = get_quiz_by_id(quiz_id, db)
    if quiz is None:
        raise HTTPException(404, "Quiz not found")
    return quiz.questions

def get_question_by_id_with_quiz(quiz_id : int, question_id : int) -> Question | None : 
    quiz = get_quiz_by_id(quiz_id)
    if quiz is None:
        return None
    for question in quiz.questions:
        if question.id == question_id:
            return question
    return None

@questions_router.get("/quizzes/{quiz_id}/questions/{question_id}")
def get_question(quiz_id: int, question_id: int)->Question:
    question = get_question_by_id_with_quiz(quiz_id=quiz_id , question_id= question_id)
    if question is None:
        raise HTTPException(404, "Question not found")
    return question

@questions_router.patch("/quizzes/{quiz_id}/questions/{question_id}")
def update_question(quiz_id : int, question_id: int, update_questionInput: QuestionInput)->Question:
    question = get_question_by_id_with_quiz(quiz_id=quiz_id, question_id=question_id)

    if question is None:
        raise HTTPException(404, "Question not found")
    
    question.text= update_questionInput.text
    question.answers= update_questionInput.answers

    return question

@questions_router.delete("/quizzes/{quiz_id}/questions/{question_id}")
def delete_question(quiz_id : int, question_id: int):
    quizz = get_quiz_by_id(quiz_id)
    if quizz is None:
        raise HTTPException(404, "Quiz not found")
    
    question = get_question_by_id_with_quiz(quiz_id=quiz_id, question_id=question_id)

    if question is None:
        raise HTTPException(404, "Question not found")
    
    quizz.questions.remove(question)
    return quizz