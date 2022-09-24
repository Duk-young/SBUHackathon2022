from typing import Optional, Literal
from pydantic import BaseModel, Field, ValidationError, validator
from datetime import datetime


class Record(BaseModel):
    recordID: int = Field(-1)
    userID: int = Field(...)
    stationID: int = Field(...)
    # createdAt: datetime = Field(datetime.isoformat(datetime.now()))
    distance: float = Field(...)
    weight: float = Field(...)