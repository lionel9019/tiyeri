# backend/chatbot/routes.py
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.user import User
from backend.core.security import get_current_user
from backend.modules.chatbot import process_user_message

router = APIRouter(prefix="/api/chatbot", tags=["Chatbot"])

@router.post("/chat")
async def chat_endpoint(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    data = await request.json()
    user_message = data.get("message", "")

    if not user_message:
        return JSONResponse(content={"reponse": "❌ Message vide."}, status_code=400)

    lang = current_user.preferred_language or "fr"
    raw_response = process_user_message(user_message, lang=lang)

    return {"reponse": raw_response}
