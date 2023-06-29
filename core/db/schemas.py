from typing import List, Union, Text
from pandas import Timestamp
from pydantic import BaseModel


class ContentBase(BaseModel):
    time: Timestamp
    content: Text
    title: Text
    writer: str

class ContentCreate(ContentBase):
    pass

class Content(ContentBase):
    id: int
    
    class Config:
        orm_mode = True

# user
class UserBase(BaseModel):
    username: str
    email: str = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    hashed_password: str
    contents: List[Content] = []
    disable: bool = False

    class Config:
        orm_mode = True

