# backend/statistics/routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.database import get_db
from backend.models.user import User
from backend.models.diagnostic import Diagnostic   # à créer si pas déjà fait
from backend.models.culture import Culture         # idem
from backend.models.zone import Zone               # idem

router = APIRouter(prefix="/api/statistics", tags=["Statistiques"])

# --- Stat globales ---
@router.get("/global")
def get_global_stats(db: Session = Depends(get_db)):
    nb_users = db.query(User).count()
    nb_diagnostics = db.query(Diagnostic).count()
    return {"utilisateurs": nb_users, "diagnostics": nb_diagnostics}

# --- Répartition par cultures ---
@router.get("/cultures")
def get_stats_by_culture(db: Session = Depends(get_db)):
    results = (
        db.query(Culture.nom, func.count(Diagnostic.id))
        .join(Diagnostic, Diagnostic.culture_id == Culture.id)
        .group_by(Culture.nom)
        .all()
    )
    return [{"culture": r[0], "nb_diagnostics": r[1]} for r in results]

# --- Répartition par maladies/affections ---
@router.get("/maladies")
def get_stats_by_maladie(db: Session = Depends(get_db)):
    results = (
        db.query(Diagnostic.maladie, func.count(Diagnostic.id))
        .group_by(Diagnostic.maladie)
        .all()
    )
    return [{"maladie": r[0], "nb_cas": r[1]} for r in results]

# --- Répartition par zones ---
@router.get("/zones")
def get_stats_by_zone(db: Session = Depends(get_db)):
    results = (
        db.query(Zone.nom, func.count(Diagnostic.id))
        .join(Diagnostic, Diagnostic.zone_id == Zone.id)
        .group_by(Zone.nom)
        .all()
    )
    return [{"zone": r[0], "nb_diagnostics": r[1]} for r in results]

# --- Répartition par pays (en supposant champ country dans User) ---
@router.get("/pays")
def get_stats_by_country(db: Session = Depends(get_db)):
    results = (
        db.query(User.country, func.count(User.id))
        .group_by(User.country)
        .all()
    )
    return [{"pays": r[0], "nb_utilisateurs": r[1]} for r in results]
