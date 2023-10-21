from sqlalchemy import ForeignKey

from schemas.base import BaseModel, Mapped, mapped_column, Base
from schemas.question import QuestionType


class Quiz(BaseModel, Base):
    __tablename__ = "quiz"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    type: Mapped[QuestionType] = mapped_column(default=QuestionType.NONE)
    points: Mapped[int] = mapped_column(default=0)
    time: Mapped[float] = mapped_column(default=0)
