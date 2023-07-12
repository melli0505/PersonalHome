from sqlalchemy.orm import Session

from core.db import models, schemas, analyzer
from core.user import user_crud

def get_content(db:Session):
    return db.query(models.Content).all()

def get_content_by_username(db: Session, username: str):
    # username에 따라 data 추출
    return db.query(models.Content).filter(models.Content.writer == username).all()

def get_content_by_id(db: Session, id: int):
    # content id에 따라 data 추출
    return db.query(models.Content).filter(models.Content.id == id).all()

def get_content_by_date(db: Session, start: str, end: str):
    # 기간에 따라 data 추출
    return db.query(models.Content).filter(models.Content.time > start, models.Content.time < end).all()

def create_content(db: Session, content: schemas.ContentCreate):

    db_user = user_crud.get_user_by_username(db=db, username=content.writer) #TODO: current user
    db_content = models.Content(time=content.time, content=content.content, title=content.title, writer=db_user.username)

    keyword_sentence = content.title + " " + content.content
    analyzer.create_keywords(contents=keyword_sentence, db=db)
    # database session에 db_user 정보 추가
    db.add(db_content)
    # db에 반영
    db.commit()
    # 최신 db 정보 
    db.refresh(db_content)
    return db_content

def create_all_keywords(db: Session):
    contents = get_content(db=db)
    for c in contents:
        keyword_sentence = c.title + " " + c.content
        analyzer.create_keywords(contents=keyword_sentence, db=db)

    return True