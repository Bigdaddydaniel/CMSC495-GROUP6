from typing import Literal
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    customer_id: str = Field(min_length=1, max_length=50)
    message: str = Field(min_length=2, max_length=1000)


class ChatResponse(BaseModel):
    conversation_id: str
    status: Literal["answered", "escalated"]
    answer: str
    confidence: float
    source: str | None = None
    ticket_id: str | None = None


class FeedbackRequest(BaseModel):
    conversation_id: str
    helpful: bool
    comment: str | None = Field(default=None, max_length=500)
