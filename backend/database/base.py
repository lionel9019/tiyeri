import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv 
from sqlalchemy.orm import sessionmaker 
# Charge .env dans backend/
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
load_dotenv(env_path)

# Lis la variable DATABASE_URL en priorité
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Sinon, reconstitue depuis variables individuelles
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME")

    if not all([DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME]):
        raise EnvironmentError("Variables DB_USER, DB_PASS, DB_HOST, DB_PORT et DB_NAME sont nécessaires dans .env")

    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Base déclarative
Base = declarative_base()

# Création moteur SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

# Session locale
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dépendance FastAPI : ouverture/fermeture auto
def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()

# Création des tables si elles n'existent pas
def create_tables():
    print("📌 Tables détectées par SQLAlchemy :", Base.metadata.tables.keys())
    Base.metadata.create_all(bind=engine)
