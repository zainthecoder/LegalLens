from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
# Try loading from parent .env.local (Next.js convention)
env_path = Path(__file__).resolve().parent.parent / '.env.local'
load_dotenv(dotenv_path=env_path)
# Also try default .env in current dir
load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
print(f"DEBUG: Loaded API Key starting with: {api_key[:10] if api_key else 'None'}")
print(f"DEBUG: Current Working Directory: {os.getcwd()}")


from api.endpoints import router as chat_router

app = FastAPI(title="LegalLens API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"], # Allow Vite and potentially Next.js if mixed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "LegalLens API is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
