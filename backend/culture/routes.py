# backend/culture/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models import AgriculturalResource, Culture, CalendrierCulture
from backend.schemas.culture import CultureCreate, CultureOut
from backend.schemas.agricultural_resource import AgriculturalResourceOut
from backend.schemas.calendrier_culture import CalendrierCultureOut

router = APIRouter(prefix="/api/cultures", tags=["Cultures"])


# --- Ressources Agricoles ---
@router.get("/resources", response_model=List[AgriculturalResourceOut])
def get_resources(db: Session = Depends(get_db)):
    """Retourne toutes les ressources agricoles disponibles."""
    return db.query(AgriculturalResource).all()


# --- Cultures ---
@router.get("/", response_model=List[CultureOut])
def get_cultures(db: Session = Depends(get_db)):
    """Retourne toutes les cultures enregistrées."""
    return db.query(Culture).all()


@router.post("/", response_model=CultureOut)
def create_culture(culture: CultureCreate, db: Session = Depends(get_db)):
    """Ajoute une nouvelle culture."""
    try:
        new_culture = Culture(**culture.dict())
        db.add(new_culture)
        db.commit()
        db.refresh(new_culture)
        return new_culture
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erreur lors de la création : {str(e)}")


# --- Calendrier par Culture ---
@router.get("/calendrier/{culture_id}", response_model=CalendrierCultureOut)
def get_calendrier(culture_id: int, db: Session = Depends(get_db)):
    """Retourne le calendrier d'une culture spécifique."""
    calendrier = db.query(CalendrierCulture).filter(
        CalendrierCulture.culture_id == culture_id
    ).first()
    if not calendrier:
        raise HTTPException(status_code=404, detail="Calendrier non trouvé")
    return calendrier
