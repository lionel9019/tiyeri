# backend/database.py

import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# URL de connexion à la base de données (doit être défini dans .env)
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise Exception("La variable d'environnement DATABASE_URL n'est pas définie dans le fichier .env")

# Création du moteur SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False  # Mets True si tu veux voir les requêtes SQL pour le debug
)

# Création de la session locale
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Déclaration de la base pour les modèles
Base = declarative_base()

# Dépendance pour injecter la session dans FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# === Modèle de la table `diagnostic_reponses` ===
class DiagnosticResponse(Base):
    __tablename__ = "diagnostic_reponses"

    id = Column(Integer, primary_key=True, index=True)
    nom_diagnostic = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    traitement = Column(Text, nullable=False)
    conseils = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

# === Fonction utilitaire : chercher un diagnostic par nom partiel ===
def get_diagnostic_response(db, diagnostic: str):
    return db.query(DiagnosticResponse).filter(
        DiagnosticResponse.nom_diagnostic.ilike(f"%{diagnostic}%")
    ).first()
