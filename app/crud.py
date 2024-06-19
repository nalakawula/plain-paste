from .database import db
from .models import Paste
from .schemas import PasteCreate
from bson import ObjectId
from datetime import datetime, timezone, timedelta

async def create_paste(paste: PasteCreate):
    new_paste = paste.model_dump()
    new_paste["created_at"] = datetime.now(timezone.utc)
    result = await db.pastes.insert_one(new_paste)
    return str(result.inserted_id)

async def get_paste(id: str):
    paste = await db.pastes.find_one({"_id": ObjectId(id)})
    if paste:
        paste["_id"] = str(paste["_id"])  # Convert ObjectId to string
        return Paste(**paste)

async def delete_paste(id: str):
    await db.pastes.delete_one({"_id": ObjectId(id)})

async def delete_expired_pastes():
    one_week_ago = datetime.now(timezone.utc) - timedelta(weeks=1)
    await db.pastes.delete_many({"created_at": {"$lt": one_week_ago}})