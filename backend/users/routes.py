# backend/users/routes.py
from fastapi import APIRouter,UploadFile, Depends,File,Form, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from backend import models
from backend.core.security import get_current_user

from backend.core.security import get_password_hash, verify_password
from backend.database import get_db
from backend.models.user import User
from backend.users import auth 

from backend.users.auth import get_current_user
from backend.schemas.user import ChangePasswordRequest
from backend.schemas.common import RegisterData, Token
from backend.core.security import (
    verify_password, get_password_hash,
    create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_user
)
import shutil, os
router = APIRouter(prefix="/api/users", tags=["Utilisateurs"])

UPLOAD_DIR = "backend/static/profile_photos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ✅ Modification du mot de passe
@router.put("/me/password")
def change_password(
    old_password: str = Form(...), 
    new_password: str = Form(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if not pwd_context.verify(old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Ancien mot de passe incorrect ❌")

    current_user.hashed_password = pwd_context.hash(new_password)
    db.commit()
    return {"message": "✅ Mot de passe changé avec succès !"}

# ✅ Upload photo de profil
@router.post("/me/profile-photo")
def upload_profile_photo(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    ext = file.filename.split(".")[-1]
    if ext.lower() not in ["jpg", "jpeg", "png"]:
        raise HTTPException(status_code=400, detail="Format non supporté ❌")

    filename = f"user_{current_user.id}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Sauvegarder chemin relatif en DB
    current_user.profile_photo = f"/static/profile_photos/{filename}"
    db.commit()

    return {"message": "✅ Photo de profil mise à jour !", "photo_url": current_user.profile_photo}

# ✅ Inscription utilisateur
@router.post("/register")
async def register(data: RegisterData, db: Session = Depends(get_db)):
    # Vérifier si l’utilisateur existe déjà
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Utilisateur déjà existant.")

    # Hacher le mot de passe
    hashed_password = get_password_hash(data.password)

    # Créer un nouvel utilisateur
    new_user = User(
        email=data.email,
        hashed_password=hashed_password,
        account_type="particulier",   # valeur par défaut
        preferred_language="fr"       # langue par défaut
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "✅ Inscription réussie", "user_id": new_user.id}


# ✅ Connexion utilisateur (JWT token)
@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Identifiants incorrects")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


# ✅ Infos utilisateur connecté
@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "account_type": current_user.account_type,
        "preferred_language": current_user.preferred_language
    }


# ✅ Préférences utilisateur
@router.post("/preferences")
async def update_preferences(
    preferences: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "account_type" in preferences:
        current_user.account_type = preferences["account_type"]

    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return {"message": "✅ Préférences mises à jour", "user": {
        "id": current_user.id,
        "account_type": current_user.account_type
    }}


# ✅ Mise à jour de la langue
@router.put("/language")
async def update_language(
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "preferred_language" not in data:
        raise HTTPException(status_code=400, detail="Langue manquante.")

    current_user.preferred_language = data["preferred_language"]
    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return {"message": "✅ Langue mise à jour", "preferred_language": current_user.preferred_language}


@router.put("/change-password")
def change_password(
    request: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Vérifie l'ancien mot de passe
    if not verify_password(request.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Ancien mot de passe incorrect")

    # Met à jour avec le nouveau mot de passe
    current_user.hashed_password = get_password_hash(request.new_password)
    db.add(current_user)
    db.commit()

    return {"message": "Mot de passe mis à jour avec succès"}

