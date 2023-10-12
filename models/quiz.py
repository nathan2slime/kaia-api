from pydantic import BaseModel

from models.question import QuestionType


class GetQuiz(BaseModel):
    type: QuestionType = QuestionType.NONE

class CreateQuiz(BaseModel):
    type: QuestionType = QuestionType.NONE
    username: str
    points: int = 0
