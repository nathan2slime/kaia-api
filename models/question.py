from typing import List
from pydantic import BaseModel

from schemas.question import QuestionType
from models.answer import CreateAnswer


class CreateQuestion(BaseModel):
    title: str
    thumb: str | None = None
    type: QuestionType = QuestionType.NONE
    answers: List[CreateAnswer]
    points: int = 10
    tip: str | None = None
