from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.database.base import Base  # ✅ base centralisée


class User(Base): 
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # Relation avec Conversation (référence par string pour éviter l'import circulaire)
    conversations = relationship("Conversation", back_populates="user")

    # Relation avec Subscription
    subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")

    account_type = Column(String(50), default="free")  # ex: free, trial, premium
    profile_photo = Column(String(255), nullable=True)  # chemin du fichier
    preferred_language = Column(String, default="fr")  # champ supplémentaire

    # relation avec Diagnostic
    diagnostics = relationship("Diagnostic", back_populates="user")