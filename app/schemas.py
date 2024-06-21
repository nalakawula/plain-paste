from pydantic import BaseModel, Field
from datetime import datetime

class PasteCreate(BaseModel):
    content: str
    burn_after_reading: bool
    expired_at: datetime

class Paste(BaseModel):
    id: str = Field(None, alias="_id")
    content: str
    created_at: datetime
