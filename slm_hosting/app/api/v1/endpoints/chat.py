from fastapi import APIRouter, HTTPException
from app.api.v1.schemas.chat import ChatCompletionRequest, ChatCompletionResponse
from app.domains.vllm_service import process_chat_intent
from app.core.exceptions import OllamaTimeOutError, OllamaConnectionError

router = APIRouter()

@router.post("/completions", response_model=ChatCompletionResponse)
async def chat_completion(request: ChatCompletionRequest):
    try:
        response = await process_chat_intent(request.message)
        return response
    except OllamaTimeOutError:
        raise HTTPException(status_code=504, detail="LLM Inference Timeout")
    except OllamaConnectionError:
        raise HTTPException(status_code=503, detail="LLM Service Unavailable")