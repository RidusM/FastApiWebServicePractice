import openrouteservice
from requests import Session
from sqlalchemy import select
from sqlalchemy.orm import session

from models import Object

token = None
with open("token.txt") as f:
    token = f.read().strip()
coords = ((8.34234,48.23424),(8.34423,48.26424))

client = openrouteservice.Client(key=token)
routes= client.directions(coords)
row = session.execute(select(Object.latitude, Object.longitude)).first()
print(row)
