from pydantic import BaseModel, Field

class ChatCompletionRequest(BaseModel):
    message: str = Field(...,max_length=500, example="Nội dung cần phân tích")

class ChatCompletionResponse(BaseModel):
    intent: str
    emotion_action: str
    latency_ms: float