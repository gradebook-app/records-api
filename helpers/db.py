import os
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(os.environ["MONGODB_URI"])
db = client.get_database("records")


def get_db():
    return db
