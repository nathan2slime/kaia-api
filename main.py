import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, desc
from database.connection import connect, engine
from models.question import CreateQuestion, QuestionType
from models.quiz import GetQuiz, CreateQuiz
from schemas.quiz import Quiz
from schemas.question import Question
from schemas.answer import Answer
from schemas.base import Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/create_question")
async def create_question(data: CreateQuestion, database: Session = Depends(connect)):
    new_question = Question(title=data.title, type=data.type, thumb=data.thumb)

    database.add(new_question)
    database.commit()

    for answer in data.answers:
        new_answer = Answer(title=answer.title, correct=answer.correct, question_id=new_question.id)

        database.add(new_answer)
        database.commit()

    question = database.query(Question).where(Question.id == new_question.id).first()

    return {**question.__dict__, "answers": question.answers}


@app.post("/get_quiz")
async def get_quiz(data: GetQuiz, database: Session = Depends(connect)):
    global questions

    if data.type == QuestionType.NONE:
        questions = (database.query(Question))
    else:
        questions = (database.query(Question).filter(Question.type == data.type))

    res = []

    for question in questions.order_by(func.random()).limit(5).all():
        res.append({**question.__dict__, "answers": question.answers})

    return res


@app.post("/create_quiz")
async def create_quiz(data: CreateQuiz, database: Session = Depends(connect)):
    new_quiz = Quiz(username=data.username, time=data.time, points=data.points, type=data.type)

    database.add(new_quiz)
    database.commit()

    return new_quiz


@app.get("/ranking")
async def ranking(database: Session = Depends(connect)):
    history = database.query(Quiz).order_by(desc(Quiz.points)).limit(70)

    return history.all()


@app.get("/healthcheck")
def healthcheck():
    return {"ok": True}


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9696)
