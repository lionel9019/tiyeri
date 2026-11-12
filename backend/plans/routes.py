# backend/plans/routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.plan import Plan

router = APIRouter(prefix="/api/plans", tags=["plans"])

@router.get("/")
def get_plans(db: Session = Depends(get_db)):
    """
    Récupère tous les plans d'abonnement disponibles.
    """
    plans = db.query(Plan).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "currency": p.currency,
            "description": p.description or f"{p.name} - {p.price} {p.currency}/mois"
        }
        for p in plans
    ]
