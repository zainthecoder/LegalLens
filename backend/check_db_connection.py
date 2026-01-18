import sys
import os
import asyncio
from dotenv import load_dotenv

# Add backend to sys.path
sys.path.append(os.path.join(os.getcwd(), "backend"))

# Load env vars
load_dotenv(os.path.join(os.getcwd(), "backend", ".env"))

async def verify():
    try:
        from core.database import init_db
        from models import User, Plan
        print("Imports successful.")
        
        print("Attempting to connect to MongoDB...")
        client = await init_db()
        print("Driver client initialized.")
        
        # Test connection by listing database names or pinging
        await client.admin.command('ping')
        print("Ping to MongoDB Atlas successful!")
        
        # Initialize Beanie (optional for this check but good practice)
        from beanie import init_beanie
        await init_beanie(database=client.get_database("legal_lens"), document_models=[User, Plan])
        print("Beanie initialization successful.")
        
    except ImportError as e:
        print(f"Import failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred during verification: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(verify())
    except Exception as e:
        print(f"Runtime error: {e}")
        sys.exit(1)
