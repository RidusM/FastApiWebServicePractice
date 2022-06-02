from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session  # type: ignore

import crud, models
from database import SessionLocal, engine
from schemas import ObjectBase

models.Base.metadata.create_all(bind=engine)
itemrouter = APIRouter()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@itemrouter.get("/objects/", response_model=List[ObjectBase])
def read_items(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    items = crud.get_items(session=session, skip=skip, limit=limit)
    return [i.serialize for i in items]


@itemrouter.get("/objects/{name}", response_model=ObjectBase)
def read_item(title: str, session: Session = Depends(get_session)):
    item = crud.get_item_by_name(session=session, title=title)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item.serialize