from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from models import ChatRequest, User
from core.llm import stream_chat
from api.auth import get_current_user

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(request: ChatRequest, current_user: User = Depends(get_current_user)):
    return StreamingResponse(
        stream_chat(request.messages),
        media_type="application/x-ndjson"
    )
