from pydantic import BaseModel

# --- Base ---
class CalendrierCultureBase(BaseModel):
    semi: str | None = None
    croissance: str | None = None
    recolte: str | None = None
    conseil_cles: str | None = None

    # ➕ Ajout des nouveaux champs
    resume: str | None = None
    infographie: str | None = None


# --- Schéma de sortie ---
class CalendrierCultureOut(CalendrierCultureBase):
    id: int
    culture_id: int

    class Config:
        from_attributes = True


# --- Schéma de création ---
class CalendrierCultureCreate(CalendrierCultureBase):
    culture_id: int
