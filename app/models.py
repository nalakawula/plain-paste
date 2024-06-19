from pydantic import BaseModel, Field
from datetime import datetime, timezone

def current_time_utc():
    return datetime.now(timezone.utc)

class Paste(BaseModel):
    id: str = Field(None, alias="_id")
    content: str
    burn_after_reading: bool
    created_at: datetime = Field(default_factory=current_time_utc)
