# backend/diagnostic/routes.py
import os
import traceback
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
#from backend.database import get_db

from backend.database.base import get_db   # ✅ Harmonisé
from backend.modules.image_analysis_module import analyze_crop_symptoms, analyze_crop_image
from backend.models.diagnostic_response import DiagnosticResponse
from backend.schemas.diagnostic_response import (
    DiagnosticResponseOut,
    DiagnosticResponseCreate,
)

router = APIRouter(prefix="/api", tags=["Diagnostic"])

# 🔎 Récupérer tous les diagnostics
@router.get("/diagnostics/", response_model=List[DiagnosticResponseOut])
def get_diagnostics(db: Session = Depends(get_db)):
    return db.query(DiagnosticResponse).all()

# 🔎 Récupérer un diagnostic par ID
@router.get("/diagnostics/{diagnostic_id}", response_model=DiagnosticResponseOut)
def get_diagnostic(diagnostic_id: int, db: Session = Depends(get_db)):
    diagnostic = db.query(DiagnosticResponse).filter(DiagnosticResponse.id == diagnostic_id).first()
    if not diagnostic:
        raise HTTPException(status_code=404, detail="Diagnostic non trouvé")
    return diagnostic

# ✅ Créer un nouveau diagnostic
@router.post("/diagnostics/", response_model=DiagnosticResponseOut, status_code=201)
def create_diagnostic(diagnostic: DiagnosticResponseCreate, db: Session = Depends(get_db)):
    db_diagnostic = DiagnosticResponse(**diagnostic.dict())
    db.add(db_diagnostic)
    db.commit()
    db.refresh(db_diagnostic)
    return db_diagnostic

# 🧪 Analyse par symptômes (texte)
@router.post("/analyse-symptomes")
def analyser_symptomes(data: dict, db: Session = Depends(get_db)):
    culture = data.get("culture")
    symptomes = data.get("symptomes", [])
    return analyze_crop_symptoms(culture, symptomes)

# 🖼️ Analyse par image
@router.post("/image/analyze", response_model=DiagnosticResponseOut)
async def analyze_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Analyse une image et retourne le diagnostic correspondant
    """
    try:
        # 📂 Sauvegarde temporaire
        temp_dir = "temp_images"
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, file.filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        # 🔮 Prédiction IA (retourne un dict, pas une string)
        prediction = analyze_crop_image(file_path)
        nom_diagnostic = prediction.get("diagnostic")

        if not nom_diagnostic:
            raise HTTPException(status_code=500, detail="⚠️ Aucun diagnostic détecté")

        # 🔍 Recherche du diagnostic exact en base
        diagnostic = db.query(DiagnosticResponse).filter(
            DiagnosticResponse.nom_diagnostic == nom_diagnostic
        ).first()

        if not diagnostic:
            raise HTTPException(
                status_code=404,
                detail=f"Diagnostic '{nom_diagnostic}' non trouvé dans la base"
            )

        # 📝 Fusionner infos BDD + IA (optionnel)
        diagnostic_out = DiagnosticResponseOut.from_orm(diagnostic)
        diagnostic_out.confiance = prediction.get("confiance")

        return diagnostic_out

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"❌ Erreur analyse image : {str(e)}"
        )

