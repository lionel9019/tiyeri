from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.database import Base, get_db
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, Index, ForeignKey

#from backend.models.conversation import Message, Conversation
from datetime import datetime

class ChatbotIntent(Base):
    __tablename__ = "chatbot_intents"

    id = Column(Integer, primary_key=True, index=True)
    intent = Column(String(255), nullable=False)
    phrase = Column(Text, nullable=False)
    langue = Column(String(255), nullable=False)
    response = Column(Text, nullable=False)
    image = Column(String(255), nullable=True)
    tags = Column(String(255), nullable=True)  # mots-clés: "agriculture,sol,nutrition"
    pending_validation = Column(Boolean, default=True, nullable=False)  # ⚡️flag apprentissage
    confidence = Column(Float, default=0.0)  # score fuzzy quand créé
    source_type = Column(String(50), default="conversation")  # ex: conversation, admin
    source_id = Column(Integer, nullable=True)  # ex: id conversation
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
 # <-- nouvelle colonne
    is_indexed = Column(Boolean, nullable=False, default=False, server_default='false')
# Index utile pour les recherches textuelles
    #Index("ix_chatbot_intents_phrase_like", ChatbotIntent.phrase)

# --- Pydantic Schema ---
class IntentCreate(BaseModel):
    intent: str
    response: str

class IntentResponse(IntentCreate):
    id: int

    class Config:
        from_attributes = True

# --- FastAPI Router ---
router = APIRouter(prefix="/intents", tags=["Chatbot Intents"])

@router.post("/", response_model=IntentResponse)
def create_intent(intent: IntentCreate, db: Session = Depends(get_db)):
    new_intent = ChatbotIntent(**intent.dict())
    db.add(new_intent)
    db.commit()
    db.refresh(new_intent)
    return new_intent

@router.get("/{intent_id}", response_model=IntentResponse)
def get_intent(intent_id: int, db: Session = Depends(get_db)):
    intent = db.query(ChatbotIntent).filter(ChatbotIntent.id == intent_id).first()
    if not intent:
        raise HTTPException(404, "Intent not found")
    return intent

class ChatbotResource(Base):
    __tablename__ = "chatbot_resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)   # ex: "dataset", "prompt", etc.
    path = Column(String(255), nullable=True)   # chemin vers un fichier si besoin
   # owner_id = Column(Integer, ForeignKey("users.id"))
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ✅ référence bien la table users
   