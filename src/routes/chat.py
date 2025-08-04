from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)
chat_router = APIRouter(prefix="/api/v1", tags=["api_v1","chat"])

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    prompt: str
    chat_history: Optional[List[ChatMessage]] = []
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None

class ChatResponse(BaseModel):
    response: str

@chat_router.post("/chat", response_model=ChatResponse)
async def chat_with_llm(request: Request, chat_req: ChatRequest):
    logger.info("Received chat request: %s", chat_req)
    try:
        # Convert ChatMessage list to dicts
        chat_history_dicts = [msg.dict() for msg in chat_req.chat_history]
        
        # Generate text using the current provider
        reply = request.app.generation_provider.generate_text(
            prompt=chat_req.prompt,
            chat_history=chat_history_dicts,
            max_output_tokens=chat_req.max_tokens,
            temperature=chat_req.temperature
        )

        return ChatResponse(response=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
