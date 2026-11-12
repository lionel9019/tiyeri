# backend/subscription/crud.py

from sqlalchemy.orm import Session
from backend.models.subscription import Subscription
from backend.schemas.subscription import SubscriptionCreate, SubscriptionUpdate
from datetime import datetime

def create_subscription(db: Session, subscription_data: SubscriptionCreate, user_id: int):
    db_subscription = Subscription(
        user_id=user_id,
        user_type=subscription_data.user_type,
        currency=subscription_data.currency,
        start_date=datetime.utcnow(),
        trial_end_date=subscription_data.trial_end_date,
        next_billing_date=subscription_data.next_billing_date,
        active=True,
        amount=subscription_data.amount,
    )
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

def update_subscription(db: Session, subscription_id: int, subscription_data: SubscriptionUpdate):
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if subscription:
        for key, value in subscription_data.dict(exclude_unset=True).items():
            setattr(subscription, key, value)
        db.commit()
        db.refresh(subscription)
    return subscription

def cancel_subscription(db: Session, subscription_id: int):
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if subscription:
        subscription.active = False
        db.commit()
        db.refresh(subscription)
    return subscription
