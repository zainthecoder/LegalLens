from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
import json
from datetime import datetime
from typing import AsyncGenerator
from beanie import PydanticObjectId 

from models import ChatRequest, User, Plan, ChatSession, Link
from core.llm import stream_chat
from api.auth import get_current_user

router = APIRouter()

async def save_and_stream(
    chat_request: ChatRequest, 
    user: User, 
    plan: Plan, 
    chat_session: ChatSession
) -> AsyncGenerator[str, None]:
    """
    Generator that:
    1. Yields 'meta' event with plan_id.
    2. Saves User message.
    3. Streams AI response (yields chunks).
    4. Accumulates AI response.
    5. Saves AI message.
    6. Updates Plan if tool called.
    """
    
    # 1. Yield Meta
    yield json.dumps({"type": "meta", "plan_id": str(plan.id)}) + "\n"
    
    # 2. Save User Message
    user_msg_content = chat_request.messages[-1]["content"] # Assuming last msg is new
    chat_session.messages.append({
        "role": "user", 
        "content": user_msg_content,
        "timestamp": datetime.utcnow().isoformat()
    })
    await chat_session.save()
    
    # 3. Stream AI
    ai_content = ""
    tool_call_args = ""
    
    async for chunk_str in stream_chat(chat_request.messages):
        yield chunk_str
        
        # Parse chunk to accumulate
        try:
            chunk = json.loads(chunk_str)
            if chunk["type"] == "text":
                ai_content += chunk["content"]
            elif chunk["type"] == "tool_chunk":
                tool_call_args += chunk["content"]
        except:
            pass
            
    # 4. Save AI Message & Execute Tool
    ai_msg = {
        "role": "assistant", 
        "content": ai_content,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if tool_call_args:
        # It was a tool call (manage_plan)
        try:
            args = json.loads(tool_call_args)
            ai_msg["tool_calls"] = [{"function": {"name": "manage_plan", "arguments": tool_call_args}}]
            
            # Update Plan in DB
            plan.title = args.get("title", plan.title)
            plan.steps = args.get("steps", plan.steps)
            plan.updated_at = datetime.utcnow()
            await plan.save()
            
        except json.JSONDecodeError:
            print("Failed to decode tool args for DB save")
            
    chat_session.messages.append(ai_msg)
    await chat_session.save()


@router.post("/chat")
async def chat_endpoint(request: ChatRequest, current_user: User = Depends(get_current_user)):
    # 1. Find or Create Plan & Session
    if request.plan_id:
        plan = await Plan.find_one(Plan.id == PydanticObjectId(request.plan_id), Plan.user_id == current_user.id)
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        chat_session = await ChatSession.find_one(ChatSession.plan_id == plan.id)
    else:
        # Create new
        plan = Plan(title="Untitled Strategy", user_id=current_user.id)
        await plan.insert()
        chat_session = ChatSession(plan_id=plan.id, user_id=current_user.id, messages=[])
        await chat_session.insert()
        
    return StreamingResponse(
        save_and_stream(request, current_user, plan, chat_session),
        media_type="application/x-ndjson"
    )
