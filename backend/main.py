from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv
from pathlib import Path
from beanie import init_beanie

# Load environment variables
env_path = Path(__file__).resolve().parent.parent / '.env.local'
load_dotenv(dotenv_path=env_path)
load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")

from api.endpoints import router as chat_router
from api.auth import router as auth_router
from api.plans import router as plans_router
from core.database import init_db
from models import User, Plan, ChatSession

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize MongoDB
    client = await init_db()
    # Initialize Beanie with all models
    await init_beanie(database=client.get_database("legal_lens"), document_models=[User, Plan, ChatSession])
    yield
    # Shutdown: (Optional) Close connection if needed, though Motor handles this well.

app = FastAPI(title="LegalLens API", lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(chat_router, prefix="/api", tags=["Chat"])
app.include_router(plans_router, prefix="/api/plans", tags=["Plans"])


@app.get("/")
async def root():
    return {"message": "LegalLens API is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
