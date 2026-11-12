# backend/schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional 

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

# Schéma utilisé pour la création d'utilisateur
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


# Schéma utilisé pour la connexion (login)
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Schéma utilisé pour l'affichage des infos utilisateur (réponse)
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  # anciennement orm_mode


# Schéma pour le token JWT renvoyé après login
class Token(BaseModel):
    access_token: str
    token_type: str


# Schéma pour extraire les infos contenues dans le token
class TokenData(BaseModel):
    email: Optional[str] = None
