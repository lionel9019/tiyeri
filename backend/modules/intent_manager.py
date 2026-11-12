from sqlalchemy.orm import Session
from backend.models import ChatbotIntent, AgriculturalResource

def match_intent_from_db(text: str, db: Session):
    text = text.lower()
    intents = db.query(ChatbotIntent).all()
    for intent in intents:
        for kw in intent.keywords.split(","):
            if kw.strip().lower() in text:
                return intent.response
    return None

def get_resource_by_culture(db: Session, culture: str):
    resources = db.query(AgriculturalResource).filter(AgriculturalResource.culture.ilike(f"%{culture}%")).all()
    if not resources:
        return None
    retour = [f"📘 {r.type.title()} : {r.contenu}" for r in resources]
    return "\n".join(retour)
