from pydantic import BaseModel

class CityInfo(BaseModel):
    ru_name: str
    en_name: str
    lat: float
    lon: float
    country: str

class City(BaseModel):
    city: str