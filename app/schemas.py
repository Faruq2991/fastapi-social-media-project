from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional, Annotated
from pydantic.types import conint

# Create a Pydantic model for the request body
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config:
        from_attributes = True


class PostCreate(PostBase):
    pass

    class Config:
        from_attributes = True

class UserOut(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class Post(PostBase):
    created_at: datetime
    user_id: int
    id: int
    owner: UserOut

    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: str
    password: str
    phone: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    is_admin: bool = False
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
    

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, conint(ge=0, le=1)]
