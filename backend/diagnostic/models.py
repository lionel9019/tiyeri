from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, func
from backend.database import Base


class DiagnosticResponse(Base):
    __tablename__ = "diagnostic_reponses"

    id = Column(Integer, primary_key=True, index=True)

    # Champs principaux
    nom_diagnostic = Column(String(255), nullable=False)
    culture = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)

    # Détails scientifiques et agronomiques
    nom_scientifique = Column(String(255), nullable=True)
    origine = Column(String(255), nullable=True)
    sol = Column(String(255), nullable=True)
    varietes = Column(Text, nullable=True)  # JSON sous forme de texte
    rendement = Column(String(255), nullable=True)

    # Nutrition et toxicité
    nutrition = Column(Text, nullable=True)  # JSON sous forme de texte
    toxicite = Column(Text, nullable=True)
    medicinal = Column(Text, nullable=True)

    # Produits et saisons
    produits = Column(Text, nullable=True)  # JSON sous forme de texte
    saisons = Column(String(255), nullable=True)

    # Conseils pratiques
    traitement = Column(Text, nullable=True)
    conseils = Column(Text, nullable=True)
    itineraire = Column(Text, nullable=True)

    # Métadonnées
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
