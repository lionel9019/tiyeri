from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.subscription import Subscription
from backend.models.user import User
from backend.schemas.subscription import SubscriptionOut
from backend.users.auth import get_current_user

router = APIRouter(
    prefix="/api/subscriptions",
    tags=["subscriptions"],
)


@router.get("/me", response_model=SubscriptionOut)
def get_my_subscription(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Vérifier si l'utilisateur a déjà un abonnement
    subscription = db.query(Subscription).filter(Subscription.user_id == current_user.id).first()

    if not subscription:
        # Créer automatiquement un abonnement gratuit d'une semaine
        subscription = Subscription(
            user_id=current_user.id,
            account_type="particulier",  # valeur par défaut
            subscription_type="essai",   # version test
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=7),
            is_active=True
        )
        db.add(subscription)
        db.commit()
        db.refresh(subscription)

    return subscription
