from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "SLM API Wrapper"
    OLLAMA_URL: str = "http://localhost:11434/v1/chat/completions"
    MODEL_NAME: str = "qwen2.5:1.5b"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()