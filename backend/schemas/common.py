# backend/schemas/common.py

from pydantic import BaseModel
from typing import Optional, List, Dict

# === Modèles Pydantic partagés ===

class NouvelleCulture(BaseModel):
    culture: str
    calendrier: Dict[str, str]   # dict bien typé
    rendement: Optional[str] = None
    conseils: Optional[str] = None


class LoginData(BaseModel):
    username: str
    password: str


class RegisterData(BaseModel):
    email: str
    password: str


class SymptomRequest(BaseModel):
    culture: str
    symptomes: List[str]


class MessageRequest(BaseModel):
    message: str


class AdminMemoryEntry(BaseModel):
    question: str
    answer: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenAdmin(BaseModel):
    access_tokenAdmin: str
    token_type: str
