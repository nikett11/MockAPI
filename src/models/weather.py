from pydantic import BaseModel

class Weather(BaseModel):
    location: dict
    temperature: float
    description: str
    forecast: list
