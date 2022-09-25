import json

import os.path
from fastapi import APIRouter, Request, Response, HTTPException, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from ..models.StationModel import Station
from datetime import datetime, timedelta
import random
# If modifying these scopes, delete the file token.json.
router = APIRouter(
    prefix="/station",
    tags=["station"],
    responses={
        404: {"description": "Not found"},
        403: {"description": "Operation forbidden"},
    },
)

@router.get("/populate")
async def populate_station(request : Request, num: int = 10):
    for i in range(num):
        newStationID = await request.app.mongodb["index"].find_one_and_update(
            {"_id": "station"}, {"$inc": {"index": 1}}, {"_id": 0}
            )
        newStationID = newStationID["index"]
        newStation = {
            "stationID":newStationID,
            "stationName": "testStation"+str(newStationID),
            "lat": round(random.uniform(0, 100), 2),
            "long": round(random.uniform(0, 100), 2)
        }
        await request.app.mongodb["station"].insert_one(newStation)

@router.get("/list")
async def get_list_of_stations(request: Request):
    stations = request.app.mongodb["station"].find({},{"_id":0})
    stations = await stations.to_list(None)
    if stations:
        return stations
    return []

@router.get("/{stationID}") #
async def get_station(request: Request, stationID: int = -1, hours : int = 12):
    station = await request.app.mongodb["station"].find_one({"stationID":stationID},{"_id":0})
    visitors = request.app.mongodb["record"].find({"createdAt":{"$gt":(datetime.now() - timedelta(hours=hours))}},{"_id":0})
    visitors = await visitors.to_list(None)
    station["visitors"] = len(visitors)
    if station:
        return station
    return None
    
@router.post("") #
async def create_station(request: Request, station: Station = Body(...)):
    station = jsonable_encoder(station)
    newStationID = await request.app.mongodb["index"].find_one_and_update(
            {"_id": "station"}, {"$inc": {"index": 1}}, {"_id": 0}
        )
    station["stationID"] = newStationID["index"]
    newStation = await request.app.mongodb["station"].insert_one(station)
    checkStation = await request.app.mongodb["station"].find_one({"stationID":station["stationID"]},{"_id":0})
    if checkStation:
        return True
    return False

            