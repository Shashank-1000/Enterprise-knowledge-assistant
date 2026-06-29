from pydantic import BaseModel, Field
from typing import Optional


class DocumentPage(BaseModel):
    document_name: str
    document_path: str
    page_number: int
    text: str


class DocumentChunk(BaseModel):
    chunk_id: str
    document_name: str
    document_path: str
    page_number: int
    chunk_index: int
    text: str
    section_title: Optional[str] = None
    metadata: dict = Field(default_factory=dict)