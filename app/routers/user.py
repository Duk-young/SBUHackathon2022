import json

import os.path
from fastapi import Depends, APIRouter, Request, Response, HTTPException, Body
from fastapi.encoders import jsonable_encoder
from ..models.UserModel import User
from .record import get_list_of_records
from datetime import datetime, timedelta
# If modifying these scopes, delete the file token.json.
router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={
        404: {"description": "Not found"},
        403: {"description": "Operation forbidden"},
    },
)

@router.get("/ranking")
async def get_user_ranking(request: Request, num:int = 5, days : int = 7, method :str ="distance"):
    group = {"$group":{
            "_id":{"userID":"$userID"},
            "userID":{"$first":"$userID"}
        }}
    if method=="distance":
        group["$group"]["totalDistance"] = {"$sum":"$distance"}
    else:
        group["$group"]["totalWeight"] = {"$sum":"$weight"}
    #rankings = request.app.mongodb[""]
    rankingData = request.app.mongodb["record"].aggregate([
        {"$match":{"createdAt":{"$gt":(datetime.now() - timedelta(days=days))}}},
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
    
@router.get("")
async def get_user(request: Request, userID: int = -1):
    user = await request.app.mongodb["user"].find_one({"userID":userID},{"_id":0})
    if user:
        user["records"] = await get_list_of_records(request, user["userID"])
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

    