import httpx
import time
import logging
from app.core.config import settings
from app.core.exceptions import OllamaTimeOutError, OllamaConnectionError
from app.api.v1.schemas.chat import ChatCompletionResponse

logger = logging.getLogger("uvicorn.error")

async def process_chat_intent(message: str) -> ChatCompletionResponse:
    start_time = time.time()
    
    system_prompt = "Chỉ trả về 1 từ duy nhất mô tả intent: 'happy', 'sad', 'angry', hoặc 'greeting'."
    payload = {
        "model": settings.MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        "temperature": 0.1,
        "max_tokens": 10
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            res = await client.post(settings.OLLAMA_URL, json=payload)
            res.raise_for_status()
            data = res.json()
            intent = data["choices"][0]["message"]["content"].strip().lower()
            
            # Mapping Logic
            action_map = {
                "happy": "nhân vật mỉm cười và nhảy múa",
                "angry": "nhân vật khoanh tay và nhíu mày",
                "sad": "nhân vật rơi nước mắt",
                "greeting": "nhân vật vẫy tay chào"
            }
            
            latency = round((time.time() - start_time) * 1000, 2)
            logger.info(f"Processed '{message[:10]}...' in {latency}ms. Intent: {intent}")
            
            return ChatCompletionResponse(
                intent=intent,
                emotion_action=action_map.get(intent, "nhân vật đứng yên"),
                latency_ms=latency
            )
            
        except httpx.ReadTimeout:
            raise OllamaTimeOutError("Model response timeout")
        except httpx.RequestError as e:
            raise OllamaConnectionError(f"Connection failed: {str(e)}")