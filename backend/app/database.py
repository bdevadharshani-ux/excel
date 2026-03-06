from motor.motor_asyncio import AsyncIOMotorClient
from app.config import config
import logging

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    
database = Database()

async def get_database():
    return database.client[config.DB_NAME]

async def connect_to_mongo():
    logger.info("Connecting to MongoDB...")
    database.client = AsyncIOMotorClient(config.MONGO_URL)
    logger.info("Connected to MongoDB successfully")

async def close_mongo_connection():
    logger.info("Closing MongoDB connection...")
    database.client.close()
    logger.info("MongoDB connection closed")