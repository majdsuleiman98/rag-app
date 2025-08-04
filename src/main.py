from fastapi import FastAPI
from routes import base, data, chat
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from stores.llm import LLMProviderFactory

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()
    app.mongodb_connect = AsyncIOMotorClient(settings.MONGO_URL)
    app.db_client = app.mongodb_connect[settings.MONGO_DATABASE]
    # Initialize LLM providers
    llm_provider_factory = LLMProviderFactory(settings)
    app.generation_provider = llm_provider_factory.create_provider(settings.GENERATION_BACKEND)
    app.generation_provider.set_generation_model(settings.GENERATION_MODEL_ID)
    app.embedding_provider = llm_provider_factory.create_provider(settings.EMBEDDING_BACKEND)
    app.embedding_provider.set_embedding_model(settings.EMBEDDING_MODEL_ID, settings.EMBEDDING_DIEMENSIONS)

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_connect.close()

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(chat.chat_router)




