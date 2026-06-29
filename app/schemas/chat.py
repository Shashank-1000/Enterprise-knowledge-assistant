from typing import List, Optional

from pydantic import BaseModel, Field


class SourceReference(BaseModel):
    document: str
    page: Optional[int] = None
    section: Optional[str] = None


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        description="User question to be answered from the enterprise knowledge base.",
    )


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceReference]
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Heuristic confidence score based on retrieval distance.",
    )
    retrieved_chunks: int
    processing_time_ms: float