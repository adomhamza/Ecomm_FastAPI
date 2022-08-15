from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr
from pydantic.types import conint


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config:
        anystr_strip_whitespace = True


class PostRespone(BaseModel):
    title: str
    content: str
    published: bool
    user_id: int
    image: Optional[str] = None

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class GetRespone(BaseModel):
    id: UUID
    title: str
    content: str
    published: bool
    user_id: int
    created_at: datetime
    image: Optional[str] = None

    owner: UserResponse

    class Config:
        orm_mode = True


class PostVoteRespone(BaseModel):
    Post: GetRespone
    votes: int


# class Arrange(BaseModel):


class User(BaseModel):
    email: EmailStr
    password: str


class Login(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: UUID
    vote_dir: conint(le=1)
