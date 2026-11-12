from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import declarative_base

from pydantic import BaseModel
Base = declarative_base()

# --- SQLAlchemy Model ---
class DiagnosticResponse(Base):
    __tablename__ = "diagnostic_reponses"

    id = Column(Integer, primary_key=True, index=True)
    nom_diagnostic = Column(String(255), index=True, nullable=False)
    description = Column(Text, nullable=True)
    traitement = Column(Text, nullable=True)
    conseils = Column(Text, nullable=True)
    culture = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


# --- Pydantic Schemas ---

class DiagnosticCreate(BaseModel):
    nom_diagnostic: str
    solution: str


class DiagnosticResponseSchema(DiagnosticCreate):
    id: int

    class Config:
        from_attributes = True
