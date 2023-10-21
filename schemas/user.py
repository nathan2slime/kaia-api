from schemas.base import BaseModel, Mapped, mapped_column, Base


class User(BaseModel, Base):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(unique=True)
    avatar: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
