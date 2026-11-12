from pydantic import BaseModel


# ==============================
# Schémas de base
# ==============================
class CultureBase(BaseModel):
    """Champs communs aux cultures"""
    nom: str


# ==============================
# Schémas d'entrée
# ==============================
class CultureCreate(CultureBase):
    """Schéma utilisé lors de la création d'une culture"""
    pass


class CultureUpdate(CultureBase):
    """Schéma utilisé lors de la mise à jour d'une culture"""
    pass


# ==============================
# Schémas de sortie
# ==============================
class CultureOut(CultureBase):
    """Schéma de sortie avec ID"""
    id: int

    class Config:
        from_attributes = True  # Compatible SQLAlchemy -> Pydantic


class CultureResponse(CultureOut):
    """Réponse API complète (peut être étendue si nécessaire)"""
    pass
