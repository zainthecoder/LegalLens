from fastapi import APIRouter, Depends, HTTPException
from typing import List
from beanie import PydanticObjectId

from models import Plan, ChatSession, User
from api.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[Plan])
async def list_user_plans(current_user: User = Depends(get_current_user)):
    """List all plans for the current user."""
    plans = await Plan.find(Plan.user_id == current_user.id).sort(-Plan.updated_at).to_list()
    return plans

@router.get("/{plan_id}")
async def get_plan_details(plan_id: PydanticObjectId, current_user: User = Depends(get_current_user)):
    """Get a specific plan and its chat history."""
    plan = await Plan.find_one(Plan.id == plan_id, Plan.user_id == current_user.id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
        
    # Fetch associated chat session
    chat_session = await ChatSession.find_one(ChatSession.plan_id == plan.id)
    
    return {
        "plan": plan,
        "chat_history": chat_session.messages if chat_session else []
    }
