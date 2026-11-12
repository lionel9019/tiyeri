# backend/culture/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models import AgriculturalResource, Culture, CalendrierCulture
from backend.schemas.culture import CultureCreate, CultureOut
from backend.schemas.agricultural_resource import AgriculturalResourceOut
from backend.schemas.calendrier_culture import CalendrierCultureOut

router = APIRouter(prefix="/api/culture", tags=["Culture"])

# ---------------------------
# 📌 Récupération des ressources agricoles
# ---------------------------
@router.get("/resources", response_model=List[AgriculturalResourceOut])
def get_resources(db: Session = Depends(get_db)):
    """Retourne toutes les ressources agricoles."""
    ressources = db.query(AgriculturalResource).all()
    return ressources

# ---------------------------
# 📌 Récupération des cultures
# ---------------------------
@router.get("/cultures", response_model=List[CultureOut])
def get_cultures(db: Session = Depends(get_db)):
    """Retourne toutes les cultures disponibles."""
    cultures = db.query(Culture).all()
    return cultures

# ---------------------------
# 📌 Récupération du calendrier cultural d’une culture donnée
# ---------------------------
@router.get("/calendrier/{culture_id}", response_model=CalendrierCultureOut)
def get_calendrier(culture_id: int, db: Session = Depends(get_db)):
    """Retourne le calendrier d'une culture spécifique."""
    calendrier = (
        db.query(CalendrierCulture)
        .filter(CalendrierCulture.culture_id == culture_id)
        .first()
    )
    if not calendrier:
        raise HTTPException(status_code=404, detail="Calendrier non trouvé")
    return calendrier
