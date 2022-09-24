from typing import Optional, Literal
from pydantic import BaseModel, Field, ValidationError, validator
from datetime import datetime


class User(BaseModel):
    userID: int = Field(...)
    username: str = Field(...)
    nickname: str = Field(...)
