import openrouteservice
from openrouteservice import convert
from requests import Session
from sqlalchemy import select
from sqlalchemy.orm import session
import sqlite3 as sl
from models import Object

token = None
with open("token.txt") as f:
    token = f.read().strip()

def db_table_select():
    conn = sl.connect('Stabis.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT longitude, latitude FROM objects")
    obInfo = [item for item in cursor.fetchall()]
    return obInfo
print(db_table_select())
client= openrouteservice.Client(key=token)
routes= client.directions(db_table_select())
print(routes)

