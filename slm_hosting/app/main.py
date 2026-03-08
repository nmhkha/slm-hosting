from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(api_router, prefix="/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to SLM API Wrapper Production"}