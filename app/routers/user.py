import json

import os.path
from fastapi import Depends, APIRouter, Request, Response, HTTPException, Body
from fastapi.encoders import jsonable_encoder
from ..models.UserModel import User
from .record import get_list_of_records
from bson import datetime as bdate
from datetime import timedelta, datetime
import random
# If modifying these scopes, delete the file token.json.
router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={
        404: {"description": "Not found"},
        403: {"description": "Operation forbidden"},
    },
)

@router.get("/populate")
async def populate_user(request : Request, num: int = 10):
    for i in range(num):
        newUserID = random.randint(0, 100000)
        newUserDict = {
            "userID":newUserID,
            "username": "testUser"+str(newUserID),
            "nickname": "testUser"+str(newUserID),
        }
        await request.app.mongodb["user"].insert_one(newUserDict)
        for j in range(10):
            newRecordID = await request.app.mongodb["index"].find_one_and_update(
            {"_id": "record"}, {"$inc": {"index": 1}}, {"_id": 0}
            )
            newRecordID = newRecordID["index"]
            newRecord = {
                "recordID":newRecordID,
                "userID": newUserID,
                "stationID": random.randint(0,10),
                "distance": round(random.uniform(0, 10), 2),
                "weight": round(random.uniform(0, 10), 2),
                "duration": datetime.now().astimezone().strftime("%H:%M:%S")
            }
            newRecord["createdAt"] = (bdate.datetime.now())
            await request.app.mongodb["record"].insert_one(newRecord)

@router.get("/ranking")
async def get_user_ranking(request: Request, num:int = 5, days : int = 7, method :str ="distance", stationID:int = -1):
    group = {"$group":{
            "_id":{"userID":"$userID"},
            "userID":{"$first":"$userID"}
        }}
    match = {"$match":{"createdAt":{"$gt":(datetime.now() - timedelta(days=days))}}}
    if stationID != -1:
        match["$match"]["stationID"] = stationID
    if method=="distance":
        group["$group"]["totalDistance"] = {"$sum":"$distance"}
    else:
        group["$group"]["totalWeight"] = {"$sum":"$weight"}
    rankingData = request.app.mongodb["record"].aggregate([
        match,
        group,
        {"$sort":{"totalDistance":-1, "totalWeight":-1}},
        {"$limit": num},
        {
                "$lookup": {
                    "from": "user",
                    "localField": "userID",
                    "foreignField": "userID",
                    "pipeline": [
                        {
                            "$project": {
                                "_id": 0,
                                "nickname": 1,
                            }
                        }
                    ],
                    "as": "userInfo",
                }
            },
        {"$project":{"_id":0, "userID":1, "nickname": {"$first": "$userInfo.nickname"},"totalWeight":1, "totalDistance":1}
        },
        ])
    rankingData = await rankingData.to_list(None)
    return rankingData
    
@router.get("/{userID}")
async def get_user(request: Request, userID: int = -1):
    user = await request.app.mongodb["user"].find_one({"userID":userID},{"_id":0})
    if user:
        user["records"] = await get_list_of_records(request, user["userID"])
        totalDistance = 0.0
        totalWeight = 0.0
        for record in user["records"]:
            totalDistance += record["distance"]
            totalWeight += record["weight"]
        user["totalWeight"] = totalWeight
        user["totalDistance"] = totalDistance
        return user
    return False

@router.post("")
async def create_user(request: Request, userInfo: User = Body(...)):
    user = jsonable_encoder(userInfo)
    newUser = await request.app.mongodb["user"].insert_one(user)
    checkUser = await get_user(request, userID=user["userID"])
    if checkUser:
        return True
    return False
            
            