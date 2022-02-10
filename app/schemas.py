from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

class PostDetails(BaseModel):
    title: str
    content: str
    published: bool = True

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    class Config:
        orm_mode = True

class User(BaseModel):
    id: int
    created_at: Optional[datetime]
    email: EmailStr
    class Config:
        orm_mode = True

class PostResponse(BaseModel):
    title: Optional [str]
    content: Optional [str]
    created_at:Optional[datetime]
    published: Optional [bool]
    id: Optional [int]
    owner: User
    class Config:
        orm_mode = True



class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


