from pydantic import BaseModel
from typing import Optional

class Event(BaseModel):
    name: str
    start_date: str
    end_date: Optional[str] = None
    location: dict
