from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class User(BaseModel):
    username: str
    email: EmailStr
    password: str


class PublicUser(BaseModel):
    model_config = ConfigDict(from_attibutes=True)
    username: str
    email: EmailStr
    id: int


class UserList(BaseModel):
    users: list[PublicUser]
