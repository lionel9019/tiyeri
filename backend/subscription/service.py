# backend/subscription/service.py

from sqlalchemy.orm import Session
from backend.models.subscription import Subscription
from backend.schemas.subscription import SubscriptionCreate, SubscriptionUpdate
from backend.subscription import crud

def create_subscription(db: Session, subscription_data: SubscriptionCreate, user_id: int):
    """Créer un abonnement pour un utilisateur"""
    return crud.create_subscription(db, subscription_data, user_id)

def update_subscription(db: Session, subscription_id: int, subscription_data: SubscriptionUpdate):
    """Mettre à jour un abonnement existant"""
    return crud.update_subscription(db, subscription_id, subscription_data)

def cancel_subscription(db: Session, subscription_id: int):
    """Annuler un abonnement (désactiver)"""
    return crud.cancel_subscription(db, subscription_id)
