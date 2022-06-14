import openrouteservice as openrouteservice
from fastapi import FastAPI
import crud
import ClarckWright
from routers import itemrouter


app = FastAPI()
app.include_router(itemrouter)