import geocoder

from aiohttp import ClientSession
from app.config import BASE_URL_OPEN_METEO
from app.schemas import SMeteo


class OpenMeteo:
    def __init__(self, city):
        self.city = city

    @property
    def params(self):
        params = {
            "latitude": geocoder.arcgis(self.city).lat,
            "longitude": geocoder.arcgis(self.city).lng,
            "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"],
            "hourly": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"],
            "daily": ["temperature_2m_min", "temperature_2m_max", "wind_speed_10m_max"],
            "wind_speed_unit": "ms",
            "forecast_hours": "6",
            "forecast_days": "3",
            "timezone": "Europe/Moscow",
        }
        return params

    async def get_meteo(self) -> SMeteo:
        async with ClientSession() as session:
            async with session.get(BASE_URL_OPEN_METEO, params=self.params) as response:
                data = await response.json()
                data = SMeteo(**data)
                return data
