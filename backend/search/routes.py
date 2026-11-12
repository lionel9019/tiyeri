# backend/search/routes.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ddgs import DDGS

from backend.database import get_db
from backend.models.agricultural_resource import AgriculturalResource


router = APIRouter(prefix="/api", tags=["Recherche"])

def search_local_knowledge(db: Session, query: str):
    return db.query(AgriculturalResource).filter(
        (AgriculturalResource.culture.ilike(f"%{query}%")) |
        (AgriculturalResource.contenu.ilike(f"%{query}%"))
    ).all()

def search_web(query: str, max_results=5):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_results)
    return [{"title": r["title"], "link": r["href"]} for r in results] if results else []

@router.get("/recherche-amelioree")
def recherche_amelioree(q: str = Query(..., min_length=3), db: Session = Depends(get_db)):
    local_results = search_local_knowledge(db, q)
    if local_results:
        return {
            "source": "locale",
            "resultats": [
                {
                    "culture": r.culture,
                    "contenu": (r.contenu[:300] + "...") if r.contenu and len(r.contenu) > 300 else (r.contenu or "")
                }
                for r in local_results
            ]
        }
    web_results = search_web(q)
    if web_results:
        return {"source": "internet", "resultats": web_results}
    return {"source": "aucun", "resultats": [], "message": "Aucun résultat trouvé"}
