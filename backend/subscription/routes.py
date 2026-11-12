from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.subscription import SubscriptionOut, SubscriptionCreate, SubscriptionUpdate
from backend.models import Subscription, User
from backend.users.auth import get_current_user
from datetime import datetime, timedelta
import logging

router = APIRouter(
    prefix="/api/subscriptions",
    tags=["subscriptions"]
)

logger = logging.getLogger(__name__)


# ---- GET : récupérer l’abonnement de l’utilisateur connecté ----
@router.get("/me", response_model=SubscriptionOut)
def get_my_subscription(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"🔎 Récupération de l'abonnement pour l'utilisateur {current_user.email}")

    subscription = (
        db.query(Subscription)
        .filter(Subscription.user_id == current_user.id)
        .first()
    )

    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucun abonnement trouvé pour cet utilisateur"
        )
    
 # ✅ on met à jour l'account_type si absent
    if not subscription.account_type:
        subscription.account_type = current_user.account_type
        db.commit()
        db.refresh(subscription)
        
    # ✅ Fallback : si account_type manquant en DB, on prend celui de current_user
    account_type = subscription.account_type or getattr(current_user, "account_type", None)

    return SubscriptionOut(
        id=subscription.id,
        user_id=subscription.user_id,
        account_type=account_type,
        start_date=subscription.start_date,
        trial_end_date=subscription.trial_end_date,
        next_billing_date=subscription.next_billing_date,
        active=subscription.active,
        subscription_status=(
            "actif" if subscription.active else "inactif"
        ),
        days_left=(
            (subscription.trial_end_date - datetime.utcnow()).days
            if subscription.trial_end_date else None
        ),
        amount=subscription.amount,
        currency=subscription.currency
    )


# ---- POST : créer un abonnement ----
@router.post("/", response_model=SubscriptionOut)
def create_subscription(
    subscription_in: SubscriptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_subscription = Subscription(
        user_id=current_user.id,
        account_type=subscription_in.account_type or current_user.account_type,
        start_date=datetime.utcnow(),
        trial_end_date=datetime.utcnow() + timedelta(days=7),
        next_billing_date=None,
        active=True,
        amount=subscription_in.amount,
        currency=subscription_in.currency
    )
    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)

    return SubscriptionOut(
        **new_subscription.__dict__,
        account_type=new_subscription.account_type
    )


# ---- PUT : mettre à jour un abonnement ----
@router.put("/me", response_model=SubscriptionOut)
def update_my_subscription(
    subscription_in: SubscriptionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    subscription = (
        db.query(Subscription)
        .filter(Subscription.user_id == current_user.id)
        .first()
    )

    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucun abonnement trouvé pour cet utilisateur"
        )

    if subscription_in.account_type is not None:
        subscription.account_type = subscription_in.account_type
    if subscription_in.amount is not None:
        subscription.amount = subscription_in.amount
    if subscription_in.active is not None:
        subscription.active = subscription_in.active
    if subscription_in.next_billing_date is not None:
        subscription.next_billing_date = subscription_in.next_billing_date

    db.commit()
    db.refresh(subscription)

    return SubscriptionOut(
        **subscription.__dict__,
        account_type=subscription.account_type or current_user.account_type
    )
