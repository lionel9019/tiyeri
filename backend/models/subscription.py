from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric, Enum, Float, Boolean
from sqlalchemy.orm import relationship
from backend.database import Base
import enum


from backend.database.base import Base
class UserTypeEnum(str, enum.Enum):
    particulier = "particulier"
    professionnel = "professionnel"


class CurrencyEnum(str, enum.Enum):
    xof = "XOF"
    eur = "EUR"
    usd = "USD"


class SubscriptionStatusEnum(str, enum.Enum):
    trial = "trial"
    active = "active"
    expired = "expired"
    canceled = "canceled"


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Relations
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=True)

    # Informations d’abonnement
    user_type = Column(Enum(UserTypeEnum), nullable=False)
    currency = Column(Enum(CurrencyEnum), nullable=False, default=CurrencyEnum.xof)
    amount = Column(Float, nullable=False, default=0.0)
    account_type = Column(String(255), nullable=True)
    # Dates
    start_date = Column(DateTime, default=datetime.utcnow)
    trial_end_date = Column(DateTime, nullable=True)       # Fin de la période d’essai
    next_billing_date = Column(DateTime, nullable=True)    # Prochaine facturation
    end_date = Column(DateTime, nullable=True)             # Fin de l’abonnement

    # Statut
    active = Column(Boolean, default=True)
    status = Column(Enum(SubscriptionStatusEnum), default=SubscriptionStatusEnum.trial)

    # Relations ORM
    user = relationship("User", back_populates="subscriptions")
    plan = relationship("Plan", back_populates="subscriptions")

 # Montant selon le type
    price = Column(Numeric(10, 2), nullable=False, default=0)

    def activate_free_trial(self):
        """Active 1 semaine gratuite."""
        self.start_date = datetime.utcnow()
        self.end_date = self.start_date + timedelta(weeks=1)
        self.price = 0
    def set_paid_plan(self):
        """Après la semaine gratuite → applique les tarifs selon user_type."""
        if self.user_type == "particulier":
            self.price = 1000
            self.currency = "XOF"
        elif self.user_type == "professionnel":
            self.price = 5000
            self.currency = "XOF"
        else:
            raise ValueError("Type d’utilisateur inconnu")

        # Nouveau cycle d’un mois
        self.start_date = datetime.utcnow()
        self.end_date = self.start_date + timedelta(days=30)