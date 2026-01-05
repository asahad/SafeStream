from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    YOUTUBE_API_KEY: str
    OPENAI_API_KEY: str

    FRONTEND_ORIGIN: str = "*"
    MAX_COMMENTS: int = 100
    MIN_SECONDS_BETWEEN_CALLS: int = 15
    CACHE_TTL_SECONDS: int = 120

settings = Settings()
