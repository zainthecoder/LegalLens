from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from beanie import Document, Link, PydanticObjectId

# --- Pydantic Models (Schemas for API) ---
class ChatRequest(BaseModel):
    messages: List[Dict[str, str]]

# --- Beanie Documents (MongoDB Collections) ---

class User(Document):
    email: str = Field(unique=True, index=True)
    hashed_password: str
    
    # Use Link for relationships in Beanie
    # Only if we really need to fetch plans from user object easily.
    # For now, we can just query plans by user_id.
    # plans: List[Link["Plan"]] = [] 

    class Settings:
        name = "users"

class Plan(Document):
    title: str
    steps: List[Dict] = [] # Storing steps as list of dicts directly
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    user_id: PydanticObjectId # Reference to User
    
    class Settings:
        name = "plans"
