
from sqlalchemy import ARRAY, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db import Base

class Answer(Base):
    __tablename__= "answers"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    is_correct = Column(Boolean)

    question_id = Column(Integer, ForeignKey("questions.id"))
    question = relationship("Question", back_populates="answers")


class Question(Base):
    __tablename__= "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)

    answers = relationship("Answer", back_populates= "question")
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    quiz = relationship("Quizz", back_populates="questions")