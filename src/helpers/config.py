from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str

    FILE_ALLOWED_TYPES: list 
    FILE_MAX_SIZE_MB: int # in MB
    FILE_DEFAULT_CHUNK_SIZE: int # in bytes
    MONGO_URL: str
    MONGO_DATABASE: str

    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str
    OPENAI_API_KEY: str = None
    OPENAI_API_URL: str = None
    COHERE_API_KEY: str = None
    GROQ_API_KEY: str = None
    GENERATION_MODEL_ID: str = None
    EMBEDDING_MODEL_ID: str = None
    EMBEDDING_DIEMENSIONS: int = None
    DEFAULT_INPUT_MAX_CHARACTERS: int = None
    DEFAULT_OUTPUT_MAX_TOKENS: int = None
    DEFAULT_TEMPERATURE: float = None

    class Config:
        env_file = ".env"

def get_settings() -> Settings:
    return Settings()