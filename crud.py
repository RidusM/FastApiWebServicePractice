from typing import List

from sqlalchemy.orm import Session  # type: ignore

from models import Object


def get_item_by_name(session: Session, title: str) -> Object:
    return session.query(Object).filter(Object.title == title).first()


def get_items(session: Session, skip: int = 0, limit: int = 100) -> List[Object]:
    return session.query(Object).offset(skip).limit(limit).all()