from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class Tweet(BaseModel):
    author_id: str # Changed from int to str to match X API example
    text: str
    username: Optional[str] = None
    id: Optional[str] = Field(default_factory=lambda: None) # Will be set by FirestoreCRUD
    created_at: Optional[str] = Field(default_factory=lambda: None) # Will be set by post_add hook
    
    # Additional fields from X API documentation
    source: Optional[Dict[str, str]] = None # Changed to Dict[str, str]
    public_metrics: Optional[Dict[str, int]] = None # e.g., {"retweet_count": 0, "reply_count": 0, "like_count": 0, "quote_count": 0}
    lang: Optional[str] = None
    possibly_sensitive: Optional[bool] = None
    entities: Optional[Dict[str, Any]] = None # e.g., {"hashtags": [], "mentions": [], "urls": []}
    referenced_tweets: Optional[List[Dict[str, str]]] = None # e.g., [{"type": "replied_to", "id": "12345"}]
    reply_settings: Optional[str] = None # e.g., "everyone", "mentionedUsers", "followers"