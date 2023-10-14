from schemas.base import BaseModel, Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey


class Answer(BaseModel, Base):
    __tablename__ = "answers"

    title: Mapped[str] = mapped_column()
    correct: Mapped[bool] = mapped_column(default=False)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
