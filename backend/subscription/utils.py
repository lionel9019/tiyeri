# backend/subscription/utils.py

from datetime import datetime, timedelta

def calculate_next_billing(start_date: datetime, cycle_days: int = 30) -> datetime:
    """Calcule la prochaine date de facturation"""
    return start_date + timedelta(days=cycle_days)

def is_trial_active(trial_end_date: datetime) -> bool:
    """Vérifie si la période d’essai est toujours active"""
    return datetime.utcnow() <= trial_end_date
