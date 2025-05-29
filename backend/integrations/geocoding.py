import httpx
from fastapi import HTTPException
from dotenv import load_dotenv
import os

from . import CityInfo, City

load_dotenv()

OPEN_WEATHER_API_TOKEN = os.getenv("OPEN_WEATHER_API_TOKEN")
OPEN_WEATHER_GEOCODE_API_URL = "http://api.openweathermap.org/geo/1.0/direct"


async def get_city_coordinates(city: City) -> CityInfo:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                OPEN_WEATHER_GEOCODE_API_URL,
                params={
                    "q": f"{city.city}",
                    "limit": 1,
                    "appid": OPEN_WEATHER_API_TOKEN
                }
            )
            geo_data = response.json()[0]

            if not geo_data:
                raise HTTPException(status_code=404, detail="Город не найден")
            return CityInfo(
                ru_name=geo_data["local_names"]['ru'],
                en_name=geo_data["local_names"]["en"],
                lat=geo_data["lat"],
                lon=geo_data["lon"],
                country=geo_data["country"]
            )
            
    except httpx.HTTPStatusError as e:
        print("Запрос не отправился)")
        raise HTTPException(
            status_code=503,
            detail=f"Ошибка геокодинга: {e.response.status_code} {e.response.text}"
        )
    except ValueError as e:
        print("Запрос не отправился)")
        raise HTTPException(
            status_code=500,
            detail=f"Некорректный формат ответа от геосервиса: {str(e)}"
        )
