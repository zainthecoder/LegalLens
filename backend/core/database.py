from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import certifi

load_dotenv()

async def init_db():
    # Retrieve the MongoDB connection string from environment variables
    mongodb_url = os.getenv("MONGODB_URL")
    
    # Strip whitespace and quotes just in case
    mongodb_url = mongodb_url.strip().strip('"').strip("'")

    if not mongodb_url.startswith("mongodb"):
        print(f"CRITICAL: Invalid MONGODB_URL. Starts with: '{mongodb_url[:8]}...' Check your Render Dashboard.")

    client = AsyncIOMotorClient(mongodb_url, tlsCAFile=certifi.where())
    database = client.get_database("legal_lens")
    
    # Import models locally to avoid circular imports if necessary, 
    # or ensure they are imported before init_beanie is called in main.py.
    # We will pass the model classes to init_beanie in main.py or here.
    # For better structure, we can just return the client/db here or do the init here if we import models.
    # Let's rely on main.py to pass the models to verify everything is loaded.
    
    return client
