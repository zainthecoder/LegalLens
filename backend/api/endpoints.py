from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from models import ChatRequest
from core.llm import stream_chat

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    return StreamingResponse(
        stream_chat(request.messages),
        media_type="application/x-ndjson"
    )
