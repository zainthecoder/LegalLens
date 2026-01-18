from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from beanie import Document, Link, PydanticObjectId

# --- Pydantic Models (Schemas for API) ---
class ChatRequest(BaseModel):
    messages: List[Dict[str, str]]
    plan_id: Optional[str] = None # Optional: ID of existing plan to continue

# --- Beanie Documents (MongoDB Collections) ---

class User(Document):
    email: str = Field(unique=True, index=True)
    hashed_password: str
    
    class Settings:
        name = "users"

class ChatSession(Document):
    plan_id: PydanticObjectId # One-to-one with Plan usually
    user_id: PydanticObjectId
    messages: List[Dict] = [] # [{"role": "user", "content": "...", "timestamp": "..."}]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "chat_sessions"

class Plan(Document):
    title: str
    steps: List[Dict] = [] 
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    user_id: PydanticObjectId
    
    class Settings:
        name = "plans"
