from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from databases import Database

DATABASE_URL = "sqlite:///Stabis.db"

@app.on_event("startup")
async def database_connect():
    await database.connect()


@app.on_event("shutdown")
async def database_disconnect():
    await database.disconnect()


@app.post("/test")
async def fetch_data(id: int):
    query = "SELECT * FROM tablename WHERE ID={}".format(str(id))
    results = await database.fetch_all(query=query)

    return  results