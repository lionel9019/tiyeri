from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from backend.database import get_db
from backend.database.base import Base
from pydantic import BaseModel

# --- SQLAlchemy Model ---
class CalendrierCulture(Base):
    __tablename__ = "calendrier_cultures"

    id = Column(Integer, primary_key=True, index=True)
    culture_id = Column(Integer, ForeignKey("cultures.id", ondelete="CASCADE"), nullable=False)

    semi = Column(String(255), nullable=True)
    croissance = Column(Text, nullable=True)
    recolte = Column(String(255), nullable=True)
    conseil_cles = Column(Text, nullable=True)
    jour_relatif = Column(Integer, nullable=True)

    # ➕ Nouveaux champs
    resume = Column(Text, nullable=True)
    infographie = Column(String(255), nullable=True)

    # Relation avec Culture
    culture = relationship("Culture", back_populates="calendriers")


# --- Pydantic Schemas ---
class CalendrierCreate(BaseModel):
    culture_id: int
    semi: str | None = None
    croissance: str | None = None
    recolte: str | None = None
    conseil_cles: str | None = None
    jour_relatif: int | None = None

    resume: str | None = None       # ➕
    infographie: str | None = None  # ➕


class CalendrierResponse(CalendrierCreate):
    id: int

    class Config:
        from_attributes = True


# --- FastAPI Router ---
router = APIRouter(prefix="/api/calendriers", tags=["Calendrier Cultural"])


@router.post("/", response_model=CalendrierResponse)
def create_calendrier(cal: CalendrierCreate, db: Session = Depends(get_db)):
    new_cal = CalendrierCulture(**cal.dict())
    db.add(new_cal)
    db.commit()
    db.refresh(new_cal)
    return new_cal


@router.get("/{culture_id}", response_model=list[CalendrierResponse])
def get_calendrier_by_culture(culture_id: int, db: Session = Depends(get_db)):
    calendriers = db.query(CalendrierCulture).filter(
        CalendrierCulture.culture_id == culture_id
    ).all()

    if not calendriers:
        raise HTTPException(status_code=404, detail="Aucun calendrier trouvé pour cette culture")

    return calendriers
