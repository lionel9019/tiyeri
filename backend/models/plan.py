from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from backend.database import Base

from backend.database.base import Base

class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False)                   # Nom du plan
    price = Column(Float, nullable=False)                       # Prix du plan
    currency = Column(String(10), nullable=False, default="XOF") # Devise (XOF, EUR, USD)
    duration_days = Column(Integer, nullable=False, default=30) # Durée en jours

    account_type = Column(String(20), nullable=False, default="particulier")  
    include_statistics = Column(Boolean, default=False)   # Accès statistiques
    include_pro_data = Column(Boolean, default=False)     # Accès données professionnelles

    description = Column(String(255), nullable=True)      # Description optionnelle

    # Relation avec Subscription
    subscriptions = relationship("Subscription", back_populates="plan")
