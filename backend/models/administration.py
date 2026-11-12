# backend/models/administration.py
from sqlalchemy import Column, Integer, String
from backend.database import Base


class Administration(Base):
    __tablename__ = "administrations"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)  # mot de passe hashé
    role = Column(String(50), nullable=False, default="administrateur")  # admin / super_admin
    description = Column(String(255), nullable=True)
