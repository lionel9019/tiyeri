# backend/schemas/diagnostic_response.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DiagnosticResponseBase(BaseModel):
    """Schéma de base pour un diagnostic"""
    nom_diagnostic: str
    description: Optional[str] = None
    traitement: Optional[str] = None
    conseils: Optional[str] = None
    solution: Optional[str] = None
    culture: Optional[str] = None


class DiagnosticResponseCreate(DiagnosticResponseBase):
    """Schéma pour la création d'un diagnostic (insertion DB)"""
    pass  # hérite déjà de tous les champs nécessaires


class DiagnosticResponseOut(DiagnosticResponseBase):
    """Schéma pour la lecture (sortie API)"""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    confiance: Optional[float] = None  # ✅ ajouté pour afficher la confiance du modèle IA

    class Config:
        from_attributes = True  # ✅ équivalent de orm_mode=True pour Pydantic v2
