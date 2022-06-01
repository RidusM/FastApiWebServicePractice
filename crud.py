from sqlalchemy.orm import Session
import models, schemas


def get_objects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Object).offset(skip).limit(limit).all()
