from pydantic import BaseModel

from models.question import QuestionType


class GetQuiz(BaseModel):
    type: QuestionType = QuestionType.NONE


class CreateQuiz(BaseModel):
    type: QuestionType = QuestionType.NONE
    user_id: int
    points: int = 0
    time: float = 0
