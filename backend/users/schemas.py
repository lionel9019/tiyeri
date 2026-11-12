from pydantic import BaseModel, EmailStr


# =====================
# ✅ Schémas de base
# =====================
class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None

    class Config:
        from_attributes = True  # ✅ SQLAlchemy -> Pydantic v2


# =====================
# ✅ Création utilisateur
# =====================
class UserCreate(UserBase):
    password: str


# =====================
# ✅ Connexion utilisateur
# =====================
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# =====================
# ✅ Sortie utilisateur
# =====================
class UserOut(UserBase):
    id: int
    account_type: str = "particulier"   # ✅ par défaut tous les comptes existants
    preferred_language: str = "fr"      # ✅ par défaut le français
    profile_photo: str | None = None    # ✅ photo de profil optionnelle


# =====================
# ✅ Token d’authentification
# =====================
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# =====================
# ✅ Préférences utilisateur
# =====================
class UserPreferences(BaseModel):
    preferred_language: str


# =====================
# ✅ Mise à jour mot de passe
# =====================
class ChangePassword(BaseModel):
    old_password: str
    new_password: str


# =====================
# ✅ Réponse mise à jour profil/photo
# =====================
class ProfilePhotoResponse(BaseModel):
    message: str
    photo_url: str
