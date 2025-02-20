from pydantic import BaseModel, EmailStr, constr, validator
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: constr(min_length=8, max_length=50)

    @validator('password')
    def password_complexity(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one number')
        return v

class UserLogin(UserBase):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class PostBase(BaseModel):
    text: constr(min_length=1, max_length=1048576)  # 1MB text limit

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class PostList(BaseModel):
    posts: List[Post] 