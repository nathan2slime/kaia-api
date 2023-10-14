from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import datetime, UTC


class Base(DeclarativeBase):
    pass


class BaseModel:
    def __tablename__(self) -> str:
        return self.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))
    deleted_at: Mapped[datetime | None]
    updated_at: Mapped[datetime | None] = mapped_column(onupdate=datetime.now(UTC))
