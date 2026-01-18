from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime

class Step(BaseModel):
    id: str = Field(..., description="Unique ID for the step")
    title: str = Field(..., description="Actionable title")
    description: Optional[str] = Field(None, description="Detailed description")
    status: Literal['pending', 'in-progress', 'done'] = 'pending'

class Plan(BaseModel):
    title: str = Field(..., description="Project title")
    steps: List[Step] = Field(default_factory=list)
    updatedAt: str = Field(default_factory=lambda: datetime.isoformat(datetime.now()))

class ChatRequest(BaseModel):
    messages: List[dict] # {role: str, content: str}
