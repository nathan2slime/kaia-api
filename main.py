from typing import Type, Annotated

import bcrypt
import uvicorn
import jwt
import datetime
from sqlalchemy import update
from fastapi import FastAPI, Header
from dotenv import dotenv_values
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, desc
from database.connection import connect, engine
from models.question import CreateQuestion, QuestionType
from models.quiz import GetQuiz, CreateQuiz
from schemas.quiz import Quiz
from models.auth import Login, SignUp
from schemas.question import Question
from schemas.answer import Answer
from schemas.user import User
from schemas.base import Base
from fastapi.middleware.cors import CORSMiddleware

env = dotenv_values(".env")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def generate_token(data: int):
    token = jwt.encode(
        {"user": data, 'typ': 'JWT', "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        env.get("JWT_SECRET"), algorithm="HS256",
    )

    return token


@app.post("/create_question")
async def create_question(data: CreateQuestion, database: Session = Depends(connect)):
    new_question = Question(title=data.title, tip=data.tip, points=data.points, type=data.type, thumb=data.thumb)

    database.add(new_question)
    database.commit()

    for answer in data.answers:
        new_answer = Answer(title=answer.title, correct=answer.correct, question_id=new_question.id)

        database.add(new_answer)
        database.commit()

    question = database.query(Question).where(Question.id == new_question.id).first()

    return {**question.__dict__, "answers": question.answers}


@app.post("/login")
async def login(data: Login, database: Session = Depends(connect)):
    try:
        user: Type[User] = database.query(User).where(User.username == data.username).first()

        if user is None:
            raise ValueError

        match = bcrypt.checkpw(data.password.encode('utf-8'), user.password)

        if match:
            token = generate_token(user.id)

            user.__dict__.pop("password")

            return {"user": user.__dict__, "token": token}
        else:
            raise ValueError
    except ValueError:
        return {"error": True, "message": "Invalid credentials"}


@app.post("/signup")
async def signup(data: SignUp, database: Session = Depends(connect)):
    try:
        exits = database.query(User).where(User.username == data.username).first()

        if exits is None:
            password = bcrypt.hashpw(data.password.encode('utf-8'), bcrypt.gensalt())

            user = User(username=data.username, avatar=data.avatar, password=password)
            database.add(user)
            database.commit()

            token = generate_token(user.id)

            user.__dict__.pop("password")

            return {"user": user.__dict__, "token": token}

        raise ValueError
    except ValueError:
        return {"error": True, "message": "User already exist"}


@app.get("/auth")
async def auth(authorization: Annotated[str | None, Header()] = None, database: Session = Depends(connect)):
    try:
        data = jwt.decode(
            str(authorization).encode('utf-8'),
            key=env.get("JWT_SECRET"),
            algorithms=["HS256"],
        )

        user = database.query(User).where(User.id == data['user']).first()
        user.__dict__.pop("password")

        return user.__dict__
    except Exception as e:
        print(e)
        return {"error": True, "message": "Session expired"}


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
    exist = (database.query(Quiz).where(Quiz.user_id == data.user_id).first())
    if exist is not None:
        exist.points = data.points
        exist.time = data.time
        exist.type = data.type

        database.commit()

        return exist
    else:
        new_quiz = Quiz(user_id=data.user_id, time=data.time, points=data.points, type=data.type)

        database.add(new_quiz)
        database.commit()

        return new_quiz


@app.get("/ranking")
async def ranking(database: Session = Depends(connect)):
    history = database.query(Quiz).order_by(desc(Quiz.points)).limit(70)

    data = history.all()
    res = []

    for i in data:
        user = database.query(User).where(User.id == i.user_id).first()

        res.append({**i.__dict__, "username": user.username, "avatar": user.avatar})

    return res


@app.get("/healthcheck")
def healthcheck():
    return {"ok": True}


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9696)
