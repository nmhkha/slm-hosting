from fastapi import APIRouter, Response, status
import httpx
from app.core.config import settings

router = APIRouter() 

@router.get("/")
async def check_health(response: Response):
    try:
        async with httpx.AsyncClient() as client:
            base_url = settings.OLLAMA_URL.split('/v1')[0]
            res = await client.get(base_url, timeout=2.0)
            return {"status": "ok", "model_server": "connected"}
    except Exception as e:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "fail", "reason": str(e)}