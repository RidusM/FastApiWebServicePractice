from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session  # type: ignore

import ClarckWright
import crud, models
import schemas
from ClarckWright import Start
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
def read_objects(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    items = crud.get_objects(session=session, skip=skip, limit=limit)
    Start()
    return [i.serialize for i in items]


@itemrouter.get("/objects/{name}", response_model=ObjectBase)
def read_objects_by_name(title: str, session: Session = Depends(get_session)):
    item = crud.get_objects_by_name(session=session, title=title)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    Start()
    return item.serialize

@itemrouter.delete("/objects/{name}")
def delete_object(title: str, session: Session = Depends(get_session)):
    item = crud.get_objects_by_name(session=session, title=title)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(item)
    session.commit()
    Start()
    return {"ok": True}

@itemrouter.post("/objects/")
def create_object(title: str, location: str, latitude: str, longitude: str, capacity:int, session: Session = Depends(get_session)):
    return crud.create_object(session, title, location, latitude, longitude, capacity)

@itemrouter.patch("/objects/{name}")
def update_object(title: str, newtitle: str, session: Session = Depends(get_session)):
    item = crud.get_objects_by_name(session=session, title=title)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item.title = newtitle
    session.add(item)
    session.commit()
    session.refresh(item)
    Start()
    return item