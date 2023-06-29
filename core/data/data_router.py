from fastapi import Depends, Form
from fastapi import APIRouter, HTTPException

from sqlalchemy.orm import Session
from typing import List
from typing_extensions import Annotated

from pandas import Timestamp

from core.db import schemas
from core.db.base import SessionLocal
from core.utils import utils

from core.data import data_crud as crud
from core.user import user_schema

from jose import jwt

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix='/api/data',
    tags=['data']
)

@router.get("/", response_model=List[schemas.Content])
def read_contents(db: Session = Depends(get_db)):
    contents = crud.get_content(db=db)
    return contents

@router.get("/{username}", response_model=List[schemas.Content])
def read_contents_by_username(username: str, db: Session = Depends(get_db)):
    contents = crud.get_content_by_username(db=db, username=username)
    return contents

@router.get("/id/{post_id}", response_model=List[schemas.Content])
def read_contents_by_id(post_id: int, db: Session = Depends(get_db)):
    contents = crud.get_content_by_id(db=db, id=post_id)
    return contents

@router.get("/date/{start}/{end}", response_model=List[schemas.Content])
def read_content_by_date(start: str, end: str, db: Session = Depends(get_db)):
    contents = crud.get_content_by_date(db=db, start=start, end=end)
    return contents

@router.post("/posting")
def create_post(title: Annotated[str, Form()], writer: Annotated[str, Form()], content: Annotated[str, Form()], time: Annotated[Timestamp, Form()], db: Session = Depends(get_db)):
    content= schemas.ContentCreate(time=time, content=content, title=title, writer=writer)
    return crud.create_content(db=db, content=content)
