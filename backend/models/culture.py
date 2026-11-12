# backend/models/culture.py
from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from backend.database.base import Base

class Culture(Base):
    __tablename__ = "cultures"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), unique=True, nullable=False)
    zone_id = Column(Integer, ForeignKey("zones.id"), nullable=True)

    # Relation avec CalendrierCulture
    calendriers = relationship( "CalendrierCulture",  back_populates="culture", cascade="all, delete-orphan")
    diagnostics = relationship("Diagnostic", back_populates="culture")
    zone = relationship("Zone", back_populates="culture")

   