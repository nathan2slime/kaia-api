from pydantic import BaseModel


class SignUp(BaseModel):
    username: str
    avatar: str
    password: str


class Login(BaseModel):
    username: str
    password: str
