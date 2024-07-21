from pydantic import BaseModel
from datetime import datetime


class SCity(BaseModel):
    name: str


class Current(BaseModel):
    time: datetime
    temperature_2m: float
    relative_humidity_2m: int
    wind_speed_10m: float


class Hourly(BaseModel):
    time: list[str]
    temperature_2m: list[float]
    relative_humidity_2m: list[float]
    wind_speed_10m: list[float]


class Daily(BaseModel):
    time: list[str]
    temperature_2m_min: list[float]
    temperature_2m_max: list[float]
    wind_speed_10m_max: list[float]

class SMeteo(BaseModel):
    timezone: str
    current: Current
    hourly: Hourly
    daily: Daily
