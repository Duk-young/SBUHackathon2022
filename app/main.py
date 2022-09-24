import os
from fastapi import FastAPI, Request, Body
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.encoders import jsonable_encoder
from .consts import origins
from .routers import user, station, record
import requests
import json

# dotenv initialize
load_dotenv()

# env var setups

DB_ADDRESS = os.getenv("DB_ADDRESS")
# initialize the app
app = FastAPI()
# routers
app.include_router(user.router)
app.include_router(station.router)
app.include_router(record.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins.urls,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(
        DB_ADDRESS + "" + "?ssl=true&ssl_cert_reqs=CERT_NONE"
    )
    app.mongodb = (
        app.mongodb_client["plogging"]
    )


@app.get("/")
async def root(request: Request):
    dbCheck = await request.app.mongodb["index"].find_one({"_id":"record"},{"_id":0})
    if dbCheck:
        return "DB successfully connected"
    return "DB not connected"
