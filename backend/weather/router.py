from fastapi import APIRouter
from integrations import get_city_weather
from . import WeatherHourlyForecast
from integrations import City

router = APIRouter()

@router.post("/weather", response_model=WeatherHourlyForecast)
async def get_weather(city: City):
    print(f"Получен город для поиска: {city.city}")
    return await get_city_weather(city)