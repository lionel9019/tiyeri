from sqlalchemy.orm import Session
from backend.models import DiagnosticResponse

def get_diagnostic_response(db: Session, nom_diagnostic: str) -> DiagnosticResponse | None:
    # Étape 1 : correspondance exacte
    #print("Connecting to DB:", SQLALCHEMY_DATABASE_URL)

    diagnostic = db.query(DiagnosticResponse).filter(
        DiagnosticResponse.nom_diagnostic == nom_diagnostic
    ).first()
    
    if diagnostic:
        return diagnostic

    # Étape 2 : correspondance approximative (tolère variations, majuscules, etc.)
    diagnostic = db.query(DiagnosticResponse).filter(
        DiagnosticResponse.nom_diagnostic.ilike(f"%{nom_diagnostic}%")
    ).first()

    return diagnostic
