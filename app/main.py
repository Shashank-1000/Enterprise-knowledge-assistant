import logging
from fastapi import FastAPI
from app.api.routes import router

from app.config.logging_config import setup_logging
# from app.config.settings import get_settings

setup_logging()
logger = logging.getLogger(__name__) # Get the logger for this module

app = FastAPI(
    title= "Enterprise Knowledge Assistant",
    description= "A production-oriented RAG assistant for answering questions from enterprise documents.",
    version= "1.0.0",
)

app.include_router(router)

@app.get("/")
def root():
    return {
        "message": "Personalized Enterprise Knowledge Assistant is running."
    }

# settings = get_settings()

# logger.info("Enterprise Assistant is starting up...")
# logger.info(f"Using model: {settings.MODEL_NAME}") 
# logger.info(f"Using Embedding model: {settings.EMBEDDING_MODEL}") 
# logger.info("Application initialized successfully.")