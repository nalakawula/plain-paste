from bson import ObjectId
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient

from .models import Paste
from .schemas import PasteCreate
from .settings import settings


client = AsyncIOMotorClient(settings.mongodb_url, connect=True)
db = client.pastebin
pastes_collection = db.pastes

async def create_paste(paste: PasteCreate):
    new_paste = paste.model_dump()
    new_paste["created_at"] = datetime.now(timezone.utc)
    result = await pastes_collection.insert_one(new_paste)
    return str(result.inserted_id)

async def get_paste(id: str):
    paste = await pastes_collection.find_one({"_id": ObjectId(id)})
    if paste:
        paste["_id"] = str(paste["_id"])  # Convert ObjectId to string
        return Paste(**paste)

async def delete_paste(id: str):
    await pastes_collection.delete_one({"_id": ObjectId(id)})

async def delete_expired_pastes():
    # delete pastes that are created last week
    # one_week_ago = datetime.now(timezone.utc) - timedelta(weeks=1)
    # await pastes_collection.delete_many({"created_at": {"$lt": one_week_ago}})

    # delete pastes that are expired
    await pastes_collection.delete_many({"expired_at": {"$lt": datetime.now(timezone.utc)}})
