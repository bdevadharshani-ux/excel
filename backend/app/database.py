from motor.motor_asyncio import AsyncIOMotorClient
from app.config import config
import logging
import certifi

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    
database = Database()

async def get_database():
    return database.client[config.DB_NAME]

async def connect_to_mongo():
    logger.info("Connecting to MongoDB...")
    try:
        # Use certifi for SSL certificate verification
        database.client = AsyncIOMotorClient(
            config.MONGO_URL,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000,
            socketTimeoutMS=10000
        )
        # Test connection
        await database.client.admin.command('ping')
        logger.info("Connected to MongoDB successfully")
    except Exception as e:
        logger.error(f"MongoDB connection failed: {e}")
        logger.info("Continuing without database connection")
        database.client = None

async def close_mongo_connection():
    logger.info("Closing MongoDB connection...")
    if database.client:
        database.client.close()
    logger.info("MongoDB connection closed")
