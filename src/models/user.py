from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    id: str = Field(..., description="Unique identifier for the user")
    name: str = Field(..., description="The name of the user")
    username: str = Field(..., description="The Twitter handle of the user")
    created_at: Optional[str] = Field(None, description="The date and time the user account was created")
    description: Optional[str] = Field(None, description="The user's profile description")
    profile_image_url: Optional[str] = Field(None, description="URL to the user's profile image")
    protected: Optional[bool] = Field(False, description="Indicates if the user's Tweets are protected")
    url: Optional[str] = Field(None, description="URL specified in the user's profile")
    verified: Optional[bool] = Field(False, description="Indicates if the user is verified")
