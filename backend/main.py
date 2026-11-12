# backend/main.py
import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# BDD
from backend.database.base import Base, engine, SessionLocal, create_tables

# Import des routes
from backend.users import routes as user_routes
from backend.chatbot import routes as chatbot_routes
from backend.administration import routes as administration_routes
from backend.culture import routes as culture_routes
from backend.diagnostic import routes as diagnostic_routes
from backend.statistics import routes as statistics_routes
from backend.search import routes as search_routes
from backend.subscription import routes as subscription_routes
from backend.conversations import routes as conversations_routes
from backend.plans import routes as plan_routes
from backend.routes import calendrier as calendrier_routes

# Charger variables d'env
load_dotenv()

# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Initialisation DB ---
try:
    create_tables()  # centralisé dans database/base.py
    logger.info("✅ Tables SQLAlchemy créées ou déjà existantes.")
except Exception as e:
    logger.error(f"❌ Erreur lors de l'initialisation de la BDD : {e}")

# --- Initialisation FastAPI ---
app = FastAPI(title="TIYERI IA API", version="0.0.9")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ à restreindre en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dossiers statiques
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/frontend", StaticFiles(directory=frontend_dir), name="frontend")
app.mount("/static", StaticFiles(directory="backend/static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

# --- Routes ---
app.include_router(user_routes.router)
app.include_router(chatbot_routes.router)
app.include_router(administration_routes.router)
app.include_router(culture_routes.router)
app.include_router(diagnostic_routes.router)
app.include_router(statistics_routes.router)
app.include_router(search_routes.router)
app.include_router(subscription_routes.router)
app.include_router(plan_routes.router)
app.include_router(conversations_routes.router)
app.include_router(calendrier_routes.router)

# --- Health check route ---
@app.get("/health")
def health_check():
    """Vérifie si l’API et la BDD fonctionnent bien."""
    try:
        db: Session = SessionLocal()
        db.execute("SELECT 1")
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        return {"status": "error", "db": str(e)}
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API TIYERI IA 🚀"}

