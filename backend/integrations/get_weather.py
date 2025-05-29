from fastapi import HTTPException
import os
import httpx
from dotenv import load_dotenv

from weather import WeatherResponse, WeatherHourlyForecast
from . import get_city_coordinates, City, CityInfo

load_dotenv()

OPEN_WEATHER_API_TOKEN = os.getenv("OPEN_WEATHER_API_TOKEN")
OPEN_WEATHER_HOURLY_FORECAST_API_URL = "https://api.openweathermap.org/data/2.5/forecast"

def prepare_weather_data(city_info: CityInfo, weather_data) -> WeatherHourlyForecast:
    return WeatherHourlyForecast(
        hourly_forecast=[
            WeatherResponse(
                city=city_info.en_name,
                country=city_info.country,
                current_temp=item['main']['temp'],
                feels_like=item['main']['feels_like'],
                description=item['weather'][0]['description'],
                humidity=item['main']['humidity'],
                pressure=item['main']['pressure'],
                wind_speed=item['wind']['speed'],
                time=item['dt']
            )
            for item in weather_data['list']
        ]
    )


async def get_city_weather(city: City) -> WeatherHourlyForecast:
    try:
        city_info = await get_city_coordinates(city)

        lat, lon = city_info.lat, city_info.lon

        async with httpx.AsyncClient() as client:
            response = await client.get(
                OPEN_WEATHER_HOURLY_FORECAST_API_URL,
                params={
                    "lat": lat,
                    "lon": lon,
                    "appid": OPEN_WEATHER_API_TOKEN,
                    "cnt": 6,
                    "units": "metric"
                }
            )
            weather_data = response.json()
            return prepare_weather_data(city_info, weather_data)
            
            
    except httpx.HTTPError as e:
        raise HTTPException(503, f"Ошибка подключения: {str(e)}")