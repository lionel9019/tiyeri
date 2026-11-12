# backend/intents/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from backend.database import get_db
from backend.models.chatbot_intent import ChatbotIntent
from backend.users.auth import get_current_user  # protège si nécessaire

router = APIRouter(prefix="/api/intents", tags=["Intents"])

class IntentUpdate(BaseModel):
    response: Optional[str] = None
    tags: Optional[str] = None
    pending_validation: Optional[bool] = None

@router.get("/pending", response_model=List[dict])
def list_pending(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    intents = db.query(ChatbotIntent).filter(ChatbotIntent.pending_validation == True).all()
    return [{
        "id": i.id,
        "phrase": i.phrase,
        "response": i.response,
        "tags": i.tags,
        "source": {"type": i.source_type, "id": i.source_id},
        "created_at": i.created_at
    } for i in intents]

@router.post("/{intent_id}/approve")
def approve_intent(intent_id: int, payload: IntentUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    intent = db.query(ChatbotIntent).get(intent_id)
    if not intent:
        raise HTTPException(status_code=404, detail="Intent introuvable")
    intent.response = payload.response or intent.response or "(réponse validée)"
    intent.tags = payload.tags or intent.tags
    intent.pending_validation = False
    db.commit()
    return {"ok": True, "id": intent.id}

@router.post("/{intent_id}/reject")
def reject_intent(intent_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    intent = db.query(ChatbotIntent).get(intent_id)
    if not intent:
        raise HTTPException(status_code=404, detail="Intent introuvable")
    db.delete(intent)
    db.commit()
    return {"ok": True, "deleted": intent_id}

@router.patch("/{intent_id}")
def update_intent(intent_id: int, payload: IntentUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    intent = db.query(ChatbotIntent).get(intent_id)
    if not intent:
        raise HTTPException(status_code=404, detail="Intent introuvable")
    if payload.response is not None:
        intent.response = payload.response
    if payload.tags is not None:
        intent.tags = payload.tags
    if payload.pending_validation is not None:
        intent.pending_validation = payload.pending_validation
    db.commit()
    return {"ok": True}
