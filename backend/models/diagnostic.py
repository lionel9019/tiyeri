# backend/models/diagnostic.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.database.base import Base 
from datetime import datetime


class Diagnostic(Base):
    __tablename__ = "diagnostics"
 
    id = Column(Integer, primary_key=True, index=True)

    maladie_detectee = Column(String(150), index=True, nullable=True)
    image_path = Column(String(255), nullable=True)  # chemin ou URL de l’image
    date_creation = Column(DateTime, default=datetime.utcnow)

    # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    culture_id = Column(Integer, ForeignKey("cultures.id"), nullable=True)
    zone_id = Column(Integer, ForeignKey("zones.id"), nullable=True)

    # Relations
    user = relationship("User", back_populates="diagnostics")
    culture = relationship("Culture", back_populates="diagnostics")
    zone = relationship("Zone", back_populates="diagnostics")

from backend.models.zone import Zone  # assure que Zone est connu avant la création
