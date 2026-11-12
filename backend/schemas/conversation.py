from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


# -------------------------
# Message Schemas
# -------------------------

class MessageBase(BaseModel):
    content: str


class MessageCreate(MessageBase):
    conversation_id: int


class MessageOut(MessageBase):
    id: int
    conversation_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# -------------------------
# Conversation Schemas
# -------------------------

class ConversationBase(BaseModel):
    title: Optional[str] = None


class ConversationCreate(ConversationBase):
    pass


class ConversationUpdate(ConversationBase):
    pass


class ConversationOut(ConversationBase):
    id: int
    created_at: datetime
    messages: List[MessageOut] = []

    class Config:
        from_attributes = True


# -------------------------
# Prompt Schema (for chatbot requests)
# -------------------------

class PromptRequest(BaseModel):
    prompt: str
    conversation_id: Optional[int] = None  # rattacher ou créer une nouvelle conversation


# -------------------------
# Response Schema (chatbot responses)
# -------------------------

class ResponseOut(BaseModel):
    response: str
    conversation_id: int
    created_at: datetime

    class Config:
        from_attributes = True
