from pydantic import BaseModel

class WeatherResponse(BaseModel):
    city: str
    country: str
    current_temp: float
    feels_like: float
    description: str
    humidity: int
    pressure: int
    wind_speed: float
    time: int

class WeatherHourlyForecast(BaseModel):
    hourly_forecast: list[WeatherResponse]