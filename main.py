from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/objects/", response_model=list[schemas.Object])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    objects = crud.get_objects(db, skip=skip, limit=limit)
    return objects