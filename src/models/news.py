from pydantic import BaseModel
from typing import Optional

class News(BaseModel):
    source: dict
    author: str
    title: str
    description: str
    url: str
    urlToImage: Optional[str] = None
    content: str
