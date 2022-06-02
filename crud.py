from typing import List

from sqlalchemy.orm import Session  # type: ignore

import models
import schemas
from models import Object


def get_objects_by_name(session: Session, title: str) -> Object:
    return session.query(Object).filter(Object.title == title).first()


def get_objects(session: Session, skip: int = 0, limit: int = 100) -> List[Object]:
    return session.query(Object).offset(skip).limit(limit).all()


def create_object(session: Session, object: schemas.ObjectCreate):
    db_objects = models.Object(title=object.title, location=object.location, latitude=object.latitude, longitude= object.longitude)
    session.add(db_objects)
    session.commit()
    session.refresh(db_objects)
    return db_objects