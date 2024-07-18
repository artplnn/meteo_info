import geocoder
import pandas as pd
import openmeteo_requests
import requests_cache
import json

from retry_requests import retry

from app.constants import BASE_URL_OPEN_METEO


class OpenMeteo:
    def __init__(self, city):
        self.cache_session = requests_cache.CachedSession(".cache", expire_after=-1)
        self.retry_session = retry(self.cache_session, retries=5, backoff_factor=0.2)
        self.om = openmeteo_requests.Client(session=self.retry_session)

        self.params = {
            "latitude": geocoder.arcgis(city).lat,
            "longitude": geocoder.arcgis(city).lng,
            "hourly": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"],
            "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"],
            "wind_speed_unit": "ms",
            "forecast_hours": "6",
        }

        self.responses = self.om.weather_api(BASE_URL_OPEN_METEO, params=self.params)
        self.response = self.responses[0]

        self.hourly = self.response.Hourly()
        self.hourly_temperature_2m = self.hourly.Variables(0).ValuesAsNumpy()
        self.hourly_data = {"datetime": pd.date_range(
            start=pd.to_datetime(self.hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(self.hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=self.hourly.Interval()),
            inclusive="left",
        ),
            "temperature_2m": self.hourly_temperature_2m,
            "relative_humidity_2m": self.hourly.Variables(1).ValuesAsNumpy(),
            "wind_speed_10m": self.hourly.Variables(2).ValuesAsNumpy(),
        }

        self.current = self.response.Current()
        self.temperature_2m = round(self.current.Variables(0).Value(), 1)
        self.relative_humidity = round(self.current.Variables(1).Value(), 1)
        self.apparent_temperature = round(self.current.Variables(2).Value(), 1)
        self.current_data = {
            "temperature_2m": self.temperature_2m,
            "relative_humidity_2m": self.relative_humidity,
            "apparent_temperature": self.apparent_temperature
        }

    async def get_hourly_data(self):
        df = pd.DataFrame(data=self.hourly_data)
        result = df.to_json(orient="index", date_format="iso", index=True)
        parsed = json.loads(result)
        return json.dumps(parsed, indent=1)

    async def get_current_data(self):
        return self.current_data
