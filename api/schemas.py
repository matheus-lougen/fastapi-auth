from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class User(BaseModel):
    username: str
    email: EmailStr
    password: str


class PublicUser(BaseModel):
    username: str
    email: EmailStr


class StoredUser(PublicUser):
    id: int


class UserList(BaseModel):
    users: list[StoredUser]
