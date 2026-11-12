# backend/models/learned_phrase.py
from backend.database import Base
from sqlalchemy import Column, Integer, Text, String, DateTime, func, Boolean
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --- SQLAlchemy Model ---
class LearnedPhrase(Base):
    __tablename__ = "learned_phrases"

    id = Column(Integer, primary_key=True, index=True)
    phrase = Column(String(255), nullable=False)
    domain = Column(String(100), nullable=True)  # ex: agriculture, santé, nutrition
    context = Column(String(255), nullable=True)
    validated = Column(Boolean, default=False)  
    created_at = Column(DateTime, default=datetime.utcnow)  # ✅ fix ici
    category = Column(String(50), default="general")   # ✅ nouveau champ
    response = Column(Text, nullable=True)   # ✅ nouvelle colonne
   
# --- Pydantic Schemas ---
class LearnedPhraseBase(BaseModel):
    phrase: str
    domain: Optional[str] = None
    context: Optional[str] = None

class LearnedPhraseCreate(LearnedPhraseBase):
    pass

class LearnedPhraseResponse(LearnedPhraseBase):
    id: int
    validated: bool
    created_at: datetime

    class Config:
        from_attributes = True   # permet de convertir SQLAlchemy -> Pydantic
