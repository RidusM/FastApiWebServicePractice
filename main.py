from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


def get_db(request: Request):
    return request.state.db


@app.get("/objects/", response_model=list[schemas.Object])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    objects = crud.get_objects(db, skip=skip, limit=limit)
    return objects
