from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class AgriculturalResource(Base):
    __tablename__ = "agricultural_resources"
    id = Column(Integer, primary_key=True, index=True)
    culture = Column(String(100), nullable=False)
    type = Column(String(100))
    contenu = Column(Text, nullable=False)

class Culture(Base):
    __tablename__ = "cultures"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), unique=True, nullable=False)

    calendriers = relationship("CalendrierCulture", back_populates="culture_rel")

class CalendrierCulture(Base):
    __tablename__ = "calendrier_cultures"
    id = Column(Integer, primary_key=True, index=True)
    culture_id = Column(Integer, ForeignKey("cultures.id"), nullable=False)

    semi = Column(String(255), nullable=True)
    croissance = Column(String(255), nullable=True)
    recolte = Column(String(255), nullable=True)
    conseil_cles = Column(Text, nullable=True)

    culture_rel = relationship("Culture", back_populates="calendriers")
