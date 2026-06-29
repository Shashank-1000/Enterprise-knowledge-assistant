from fastapi import APIRouter, HTTPException

from app.services.knowledge_assistant import KnowledgeAssistantService
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()
assistant = KnowledgeAssistantService()

@router.post("/ask", response_model=ChatResponse)
def ask_question(request: ChatRequest):
    try:
        return assistant.answer_question(request.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail= f"Failed to generate answer: {str(e)}",)