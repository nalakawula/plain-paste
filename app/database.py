from motor.motor_asyncio import AsyncIOMotorClient
from .settings import settings

client = AsyncIOMotorClient(settings.mongodb_url, connect=True)
db = client.pastebin
