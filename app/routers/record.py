import json

import os.path
from fastapi import APIRouter, Request, Response, HTTPException, Body
from fastapi.encoders import jsonable_encoder
from bson import datetime
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from ..models.RecordModel import Record
# If modifying these scopes, delete the file token.json.
router = APIRouter(
    prefix="/record",
    tags=["record"],
    responses={
        404: {"description": "Not found"},
        403: {"description": "Operation forbidden"},
    },
)

@router.get("/list") #
async def get_list_of_records(request: Request, userID: int = -1):
    records = request.app.mongodb["record"].find({"userID":userID},{"_id":0, "recordID":1, "userID":1,"stationID":1, "distance":1, "weight":1, "duration":1})
    records = await records.to_list(None)
    for record in records:
        record["createdAt"] = (record["createdAt"]).astimezone().strftime("%Y-%m-%d %H:%M:%S")
    if records:
        return records
    return []

@router.get("/{recordID}") #
async def get_record(request: Request, recordID: int = -1):
    record = await request.app.mongodb["record"].find_one({"recordID":recordID},{"_id":0, "recordID":1, "userID":1,"stationID":1, "distance":1, "weight":1, "duration":1, "checkPoints":1})
    if record:
        record["createdAt"] = (record["createdAt"]).astimezone().strftime("%Y-%m-%d %H:%M:%S")
        return record
    return None

@router.post("") #
async def create_record(request: Request, Record: Record = Body(...)): 
    record = jsonable_encoder(Record)
    newRecordID = await request.app.mongodb["index"].find_one_and_update(
            {"_id": "record"}, {"$inc": {"index": 1}}, {"_id": 0}
        )
    record["recordID"] = newRecordID["index"]
    record["createdAt"] = (datetime.datetime.now())
    newRecord = await request.app.mongodb["record"].insert_one(record)
    checkRecord = await request.app.mongodb["record"].find_one({"recordID":record["recordID"]},{"_id":0})
    if checkRecord:
        return True
    return False

