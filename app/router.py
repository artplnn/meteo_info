from fastapi import APIRouter, Depends

from app.openmeteo import OpenMeteo
from app.schemas import City


router = APIRouter()


@router.post("/search_hourly")
async def get_temperature_from_city(city: City = Depends()):
    return await OpenMeteo(city.name).get_hourly_data()


@router.post("/search_current")
async def get_current_temperature_from_city(city: City = Depends()):
    return await OpenMeteo(city.name).get_current_data()
