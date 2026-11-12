# --- AJOUTS EN HAUT DU FICHIER ---
from fastapi import BackgroundTasks
from sqlalchemy import select
from models import IntentDef, Knowledge, QueryLog, norm_hash, Plant  # Plant si tu l'as
from ml.nlu import NLU, load_intents, normalize, extract_plant_candidate
from ml.web_sources import search_plant_online
import json

# --- Charger exemples d'intentions depuis la DB (si vide = défaut) ---
def _load_intents_from_db(db: Session):
    rows = db.query(IntentDef).all()
    if not rows:
        return {}
    return {r.name: r.examples() for r in rows}

with SessionLocal() as _db:
    _intents = load_intents(_load_intents_from_db(_db))
nlu = NLU(_intents)

# --- Helpers de persistance ---
def _save_knowledge_async(db: Session, intent: str, q_norm: str, raw_query: str, answer: dict, source: str):
    k = Knowledge(
        intent_name=intent,
        query_text=raw_query,
        query_norm_hash=norm_hash(q_norm),
        answer_json=json.dumps(answer, ensure_ascii=False),
        source=source
    )
    db.add(k)
    db.commit()

def _log_query_async(db: Session, raw: str, norm: str, intent: str, conf: float, resolved: bool):
    db.add(QueryLog(
        user_query=raw,
        normalized=norm,
        predicted_intent=intent,
        confidence=conf,
        resolved=1 if resolved else 0
    ))
    db.commit()

# --- Schémas ---
class AskIn(BaseModel):
    query: str

class AskOut(BaseModel):
    intent: str
    confidence: float
    entities: dict
    result: dict
    source: str  # local|web|cached

# --- ROUTE PRINCIPALE ---
@app.post("/nlu/ask", response_model=AskOut)
def nlu_ask(payload: AskIn, background: BackgroundTasks, db: Session = Depends(get_db)):
    raw = payload.query
    qn = normalize(raw)

    # 1) INTENT
    intent, conf = nlu.predict_intent(raw)

    # 2) CACHE
    key = norm_hash(qn + "|" + intent)
    cached = db.query(Knowledge).filter(Knowledge.query_norm_hash == key).first()
    if cached:
        background.add_task(_log_query_async, db, raw, qn, intent, conf, True)
        return AskOut(intent=intent, confidence=conf, entities={}, result=json.loads(cached.answer_json), source="cached")

    # 3) ENTITÉS (nom de plante) — heuristique + fallback
    plant_guess = extract_plant_candidate(qn)

    # 4) RÉSOLUTION LOCALE SELON INTENT
    result, source = None, "local"

    if intent == "ask_scientific_name":
        sci = None

        # a) local DB 'plants' si dispo
        if plant_guess:
            p = db.query(Plant).filter(
                (Plant.common_name.ilike(f"%{plant_guess}%")) |
                (Plant.scientific_name.ilike(f"%{plant_guess}%"))
            ).first() if "Plant" in globals() else None
            if p:
                sci = p.scientific_name

        if not sci:
            # b) fallback web (GBIF+Wikipedia)
            web = search_plant_online(plant_guess or raw)
            if web and web.get("scientific_name"):
                result = {"scientific_name": web["scientific_name"], "family": web.get("family"), "summary": web.get("summary"), "ref": web.get("reference_url")}
                source = "web"
                # upsert Plant si table dispo
                if "Plant" in globals() and plant_guess:
                    existing = db.query(Plant).filter(Plant.scientific_name == web["scientific_name"]).first()
                    if not existing:
                        db.add(Plant(
                            scientific_name=web["scientific_name"],
                            common_name=plant_guess,
                            plant_type="",
                            family=web.get("family") or "",
                            description=web.get("summary") or ""
                        ))
                        db.commit()
            elif sci:
                result = {"scientific_name": sci}
            else:
                result = {"message": "Aucune correspondance trouvée — reformulez ou précisez la plante."}

    elif intent == "ask_plant_types":
        # Liste statique locale (à enrichir) — ou ressources web
        result = {"types": ["Arbre", "Arbuste", "Herbacée", "Liane", "Céréale", "Légumineuse", "Tubercule", "Fruitier"]}
    elif intent == "ask_family":
        web = search_plant_online(plant_guess or raw)
        if web and (web.get("family") or web.get("scientific_name")):
            result = {"plant": plant_guess, "family": web.get("family"), "scientific_name": web.get("scientific_name"), "ref": web.get("reference_url")}
            source = "web"
        else:
            result = {"message": "Famille introuvable pour cette requête."}
    elif intent == "ask_uses":
        # Wikipedia résume souvent les usages
        web = search_plant_online(plant_guess or raw)
        if web and web.get("summary"):
            result = {"plant": plant_guess, "uses_summary": web["summary"], "ref": web.get("reference_url")}
            source = "web"
        else:
            result = {"message": "Usages non trouvés."}
    else:
        # Fallback global — essaie web directement
        web = search_plant_online(plant_guess or raw)
        if web:
            result = web
            source = "web"
        else:
            result = {"message": "Intent non compris et aucune source trouvée."}

    # 5) Sauvegarde cache + log en background
    resolved = result is not None
    background.add_task(_log_query_async, db, raw, qn, intent, conf, resolved)
    background.add_task(_save_knowledge_async, db, intent, qn + "|" + intent, raw, result or {}, source)

    return AskOut(intent=intent, confidence=conf, entities={"plant": plant_guess}, result=result or {}, source=source)
