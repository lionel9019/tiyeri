from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from backend.models.subscription import UserTypeEnum, CurrencyEnum


# ---- Base commune ----
class SubscriptionBase(BaseModel):
    user_type: Optional[UserTypeEnum] = None  # ✅ rendu optionnel
    currency: Optional[CurrencyEnum] = None
    start_date: Optional[datetime] = None
    trial_end_date: Optional[datetime] = None
    next_billing_date: Optional[datetime] = None
    active: bool = True
    amount: Optional[float] = None
    account_type: Optional[str] = None
    
    class Config:
        from_attributes = True  # Pydantic v2


# ---- Création ----
class SubscriptionCreate(SubscriptionBase):
    user_id: int


# ---- Mise à jour ----
class SubscriptionUpdate(BaseModel):
    user_type: Optional[UserTypeEnum] = None
    currency: Optional[CurrencyEnum] = None
    start_date: Optional[datetime] = None
    trial_end_date: Optional[datetime] = None
    next_billing_date: Optional[datetime] = None
    active: Optional[bool] = None
    amount: Optional[float] = None

    class Config:
        from_attributes = True


# ---- Sortie (lecture) ----
class SubscriptionOut(SubscriptionBase):
    id: int
    user_id: int
    start_date: datetime
    trial_end_date: Optional[datetime] = None
    next_billing_date: Optional[datetime] = None
    active: bool
    amount: Optional[float] = None

    # champs supplémentaires
    account_type: Optional[str] = None   # ✅ cohérent avec User
    days_left: Optional[int] = None      # ✅ calculé dans la route

    class Config:
        from_attributes = True


# ---- Plan (lecture seule) ----
class PlanOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    currency: CurrencyEnum
    duration_days: int

    class Config:
        from_attributes = True
