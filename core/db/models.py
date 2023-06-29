from sqlalchemy import Boolean, Column, ForeignKey,  Integer, String, TIMESTAMP, Float, Text
from sqlalchemy.orm import relationship

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from .base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, index=True)
    disable = Column(Boolean, index=True, default=False)

class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(TIMESTAMP, index=True)
    title = Column(Text, index=True)
    content = Column(Text, index=True)
    writer = Column(String, ForeignKey("users.username"))
