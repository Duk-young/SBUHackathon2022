import json

import os.path
from fastapi import Depends, APIRouter, Request, Response, HTTPException, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse
from bson import ObjectId
from typing import List
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from pydantic.types import Json
from ..models.UserModel import User
from .record import get_list_of_records
# If modifying these scopes, delete the file token.json.
router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={
        404: {"description": "Not found"},
        403: {"description": "Operation forbidden"},
    },
)

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

    