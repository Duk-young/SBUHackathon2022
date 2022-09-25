from typing import Optional, Literal
from pydantic import BaseModel, Field, ValidationError, validator
from datetime import datetime


class Station(BaseModel):
    stationID: int = Field(-1)
    stationName: str = Field(...)
    lat: float = Field(...)
    long: float = Field(...)
    address: str = Field("")
