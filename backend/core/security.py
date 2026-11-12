# backend/core/security.py
from datetime import datetime, timedelta
from jose import JWTError, jwt, ExpiredSignatureError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import os

from backend.database import get_db
from backend.models.user import User
from backend.models.administration import Administration

# =============================
# ⚙️ CONFIGURATION SÉCURITÉ
# =============================
SECRET_KEY = os.getenv("SECRET_KEY", "tiyeri-secret")  # clé centralisée
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/token")
oauth_admin_scheme = OAuth2PasswordBearer(tokenUrl="/api/admin/token")

# =============================
# 🔑 GESTION DES MOTS DE PASSE
# =============================
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# =============================
# 🔑 GÉNÉRATION DE TOKEN
# =============================
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_access_token_admin(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# =============================
# 👤 DÉPENDANCES UTILISATEURS
# =============================
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Utilisateur non reconnu. Veuillez vous reconnecter.",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expirée. Merci de vous reconnecter.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError as e:
        print("❌ JWTError (user):", str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide. Merci de vous reconnecter.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.email == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur introuvable. Merci de vous reconnecter.",
        )
    return user

# =============================
# 👑 DÉPENDANCES ADMIN
# =============================
async def get_current_admin(token: str = Depends(oauth_admin_scheme), db: Session = Depends(get_db)) -> Administration:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Administrateur non reconnu. Veuillez vous reconnecter.",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session administrateur expirée. Merci de vous reconnecter.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError as e:
        print("❌ JWTError (admin):", str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token administrateur invalide.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    admin = db.query(Administration).filter(Administration.username == username).first()
    if not admin or admin.role.lower() not in ["administrateur", "super_admin"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Accès administrateur refusé.",
        )
    return admin
