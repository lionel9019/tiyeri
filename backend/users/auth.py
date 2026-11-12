# backend/users/auth.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext  # ✅ correction manquante
import os

from backend.database import get_db
from backend import models
from backend.schemas import user as schemas
from backend.core.security import verify_password, get_password_hash  # centralisation sécurité

# === Configuration JWT ===
SECRET_KEY = os.getenv("SECRET_KEY", "tiyeri-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Gestion du hashage de mot de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # ✅ ajouté

# OAuth2 (utilisateurs)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/token")  # ✅ corrigé le chemin
# OAuth2 (admins)
oauth_admin_scheme = OAuth2PasswordBearer(tokenUrl="/api/admin/token")

# === Fonctions pour JWT ===
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Créer un JWT pour utilisateur"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_access_token_admin(data: dict, expires_delta: timedelta | None = None):
    """Créer un JWT pour administrateur"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# === Dépendances ===
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Récupère l'utilisateur connecté via son token"""
    print("🔑 Vérification du token:", token[:20] + "...")  # debug: affiche début du token
    print(f"🔎 Header reçu = {token}")
    credentials_exception = HTTPException(
        status_code=401,
        detail="Impossible de valider l'identité",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as e:
        print("❌ JWTError:", str(e))
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.email == username).first()
    if not user:
        raise credentials_exception
    return user

async def get_current_admin(token: str = Depends(oauth_admin_scheme), db: Session = Depends(get_db)):
    """Récupère l'admin connecté via son token"""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Identifiants administrateur invalides",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    admin = db.query(models.Administration).filter(models.Administration.username == username).first()
    if not admin or admin.role.lower() not in ["administrateur", "super_admin"]:
        raise credentials_exception
    return admin
