# backend/models/agricultural_resource.py
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from backend.database import Base


class AgriculturalResource(Base):
    __tablename__ = "agricultural_resources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
