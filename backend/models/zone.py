# backend/models/zone.py
from sqlalchemy import Column, Integer, String
from backend.database.base import Base


from sqlalchemy.orm import relationship
class Zone(Base):
    __tablename__ = "zones"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), unique=True, index=True, nullable=False)

    diagnostics = relationship("Diagnostic", back_populates="zone", cascade="all, delete-orphan")
  
    culture = relationship("Culture", back_populates="zone")