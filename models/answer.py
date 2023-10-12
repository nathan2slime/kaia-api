from pydantic import BaseModel


class CreateAnswer(BaseModel):
    title: str
    correct: bool = False

