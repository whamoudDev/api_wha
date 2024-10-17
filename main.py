from fastapi import FastAPI # type: ignore

import quizzes.crud
import questions.crud

from db import engine
from questions import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(quizzes.crud.quizzes_router)
app.include_router(questions.crud.questions_router)

@app.get("/")
def read_root():
    """Return coucou"""
    return {"message": "Hello, World!"}

