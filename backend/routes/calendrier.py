from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
#from backend.database.utils import get_db

from backend.database import  get_db
from backend.models.calendrier_culture import CalendrierCulture
from backend.models.agricultural_resource import AgriculturalResource

router = APIRouter(prefix="/api/calendrier", tags=["Calendrier"])

# ✅ Données statiques en mémoire (optionnelles)

calendar_data = {
 
    "tomate": [
        {"étape": "semis", "jours_après_semis": 0},
        {"étape": "repiquage", "jours_après_semis": 21},
        {"étape": "fertilisation bio", "jours_après_semis": 28},
        {"étape": "floraison", "jours_après_semis": 50},
        {"étape": "récolte", "jours_après_semis": 75},
    ],
      "maïs": [
            {"étape": "semis (engrais organique conseillé)", "jours_après_semis": 0},
            {"étape": "désherbage (manuel ou mécanique)", "jours_après_semis": 15},
            {"étape": "apport compost phosphore", "jours_après_semis": 18},
            {"étape": "buttage", "jours_après_semis": 30},
            {"étape": "floraison", "jours_après_semis": 55},
            {"étape": "récolte", "jours_après_semis": 90}
        ],
        "maïs hybride": [
            {"étape": "semis (avec engrais starter si possible)", "jours_après_semis": 0},
            {"étape": "levée", "jours_après_semis": 7},
            {"étape": "croissance rapide (apport azote recommandé)", "jours_après_semis": 21},
            {"étape": "floraison", "jours_après_semis": 50},
            {"étape": "récolte", "jours_après_semis": 95}
        ],
        "igname": [
            {"étape": "plantation (engrais organique fortement conseillé)", "jours_après_semis": 0},
            {"étape": "montaison", "jours_après_semis": 45},
            {"étape": "développement tubercule", "jours_après_semis": 90},
            {"étape": "récolte", "jours_après_semis": 240}
        ],
        "patate douce": [
            {"étape": "plantation (avec compost ou fumier)", "jours_après_semis": 0},
            {"étape": "développement des tiges", "jours_après_semis": 20},
            {"étape": "grossissement tubercules (engrais potassique possible)", "jours_après_semis": 70},
            {"étape": "récolte", "jours_après_semis": 120}
        ],
        "oignon": [
            {"étape": "semis (sol enrichi au compost)", "jours_après_semis": 0},
            {"étape": "grossissement bulbe (azote modéré)", "jours_après_semis": 60},
            {"étape": "récolte", "jours_après_semis": 100}
        ],
        "laitue": [
            {"étape": "semis (apport initial compost)", "jours_après_semis": 0},
            {"étape": "repiquage", "jours_après_semis": 15},
            {"étape": "formation des feuilles (engrais azoté modéré)", "jours_après_semis": 35},
            {"étape": "récolte", "jours_après_semis": 60}
        ],
        "chou": [
            {"étape": "semis (compost conseillé)", "jours_après_semis": 0},
            {"étape": "repiquage", "jours_après_semis": 25},
            {"étape": "pommage (apport régulier de compost ou engrais)", "jours_après_semis": 55},
            {"étape": "récolte", "jours_après_semis": 85}
        ],
        "carotte": [
            {"étape": "semis (apport compost préalable)", "jours_après_semis": 0},
            {"étape": "levée", "jours_après_semis": 30},
            {"étape": "développement racinaire (engrais potassique conseillé)", "jours_après_semis": 60},
            {"étape": "récolte", "jours_après_semis": 90}
        ],
        "aubergine": [
            {"étape": "semis (sol riche conseillé)", "jours_après_semis": 0},
            {"étape": "repiquage", "jours_après_semis": 30},
            {"étape": "floraison (apport compost/engrais équilibré)", "jours_après_semis": 60},
            {"étape": "récolte", "jours_après_semis": 90}
        ],
        "pomme fruit": [
            {"étape": "floraison (apports printaniers compost/engrais)", "jours_après_semis": 0},
            {"étape": "nouaison", "jours_après_semis": 30},
            {"étape": "grossissement", "jours_après_semis": 70},
            {"étape": "récolte", "jours_après_semis": 120}
        ],
        "blé": [
            {"étape": "semis (préparation avec engrais phosphaté)", "jours_après_semis": 0},
            {"étape": "tallage", "jours_après_semis": 20},
            {"étape": "montaison (azote)", "jours_après_semis": 40},
            {"étape": "épiaison", "jours_après_semis": 70},
            {"étape": "récolte", "jours_après_semis": 100}
        ],
        "sorgho": [
            {"étape": "semis (compost ou NPK organique conseillé)", "jours_après_semis": 0},
            {"étape": "levée", "jours_après_semis": 12},
            {"étape": "floraison", "jours_après_semis": 55},
            {"étape": "remplissage des grains", "jours_après_semis": 75},
            {"étape": "récolte", "jours_après_semis": 110}
        ],
        "mil": [
            {"étape": "semis (sol bien amendé conseillé)", "jours_après_semis": 0},
            {"étape": "levée", "jours_après_semis": 10},
            {"étape": "tallage", "jours_après_semis": 30},
            {"étape": "floraison", "jours_après_semis": 60},
            {"étape": "récolte", "jours_après_semis": 100}
        ],
        "coton": [
            {"étape": "semis (sol fertile, compost ou NPK conseillé)", "jours_après_semis": 0},
            {"étape": "croissance végétative", "jours_après_semis": 30},
            {"étape": "floraison", "jours_après_semis": 60},
            {"étape": "maturité", "jours_après_semis": 100},
            {"étape": "récolte", "jours_après_semis": 140}
        ],
        "soja": [
            {"étape": "semis (compost ou engrais à base de phosphore)", "jours_après_semis": 0},
            {"étape": "levée", "jours_après_semis": 7},
            {"étape": "floraison", "jours_après_semis": 35},
            {"étape": "formation des gousses", "jours_après_semis": 55},
            {"étape": "récolte", "jours_après_semis": 90}
        ],
        "papaye": [
            {"étape": "plantation (apport compost ou fumier mûr)", "jours_après_semis": 0},
            {"étape": "floraison", "jours_après_semis": 90},
            {"étape": "fructification", "jours_après_semis": 150},
            {"étape": "récolte", "jours_après_semis": 210}
        ],
        "orangier": [
            {"étape": "floraison (fertilisation équilibrée régulière)", "jours_après_semis": 0},
            {"étape": "fructification", "jours_après_semis": 60},
            {"étape": "maturité", "jours_après_semis": 120},
            {"étape": "récolte", "jours_après_semis": 150}
        ],
        "manguier kent": [
            {"étape": "floraison (avec compost ou NPK)", "jours_après_semis": 0},
            {"étape": "nouaison", "jours_après_semis": 40},
            {"étape": "grossissement", "jours_après_semis": 70},
            {"étape": "récolte", "jours_après_semis": 120}
        ]
        
    # Ajouter plus de cultures ici
}

# 🔹 Route calendrier calculé en mémoire
@router.get("/generate")
def get_calendar(culture: str = Query(...), date_semis: str = Query(...)):
    if culture.lower() not in calendar_data:
        raise HTTPException(status_code=404, detail="Culture inconnue")
    try:
        semis_date = datetime.strptime(date_semis, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Format de date invalide. Utilisez YYYY-MM-DD")

    calendrier = []
    for étape in calendar_data[culture.lower()]:
        action_date = semis_date + timedelta(days=étape["jours_après_semis"])
        calendrier.append({"étape": étape["étape"], "date": action_date.strftime("%Y-%m-%d")})

    return {"calendrier": calendrier}

# 🔹 2. Récupérer toutes les ressources (liste)
@router.get("/")
def get_calendrier(db: Session = Depends(get_db)):
    ressources = db.query(AgriculturalResource).order_by(AgriculturalResource.culture.asc()).all()
    return [
        {
            "culture": r.culture,
            "calendrier": getattr(r, "calendrier", {}),
            "rendement": getattr(r, "rendement", ""),
            "conseils": getattr(r, "conseils", ""),
            "resume": getattr(r, "resume", ""),           # ➕
            "infographie": getattr(r, "infographie", "")  # ➕
        }
        for r in ressources
    ]




# 🔹 3. Récupérer calendrier détaillé d’une culture
@router.get("/{culture_id}")
def get_calendrier_by_culture(culture_id: int, db: Session = Depends(get_db)):
    cal = db.query(CalendrierCulture).filter(CalendrierCulture.culture_id == culture_id).first()
    if not cal:
        raise HTTPException(status_code=404, detail="Calendrier non trouvé")
    return {
        "semi": cal.semi or "-",
        "croissance": cal.croissance or "-",
        "recolte": cal.recolte or "-",
        "conseil_cles": cal.conseil_cles or "-",
        "resume": cal.resume or "",              # ➕
        "infographie": cal.infographie or ""     # ➕
    }
