from logging.config import fileConfig
import os
import sys
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from alembic import context

# --- Ajouter le projet au PYTHONPATH ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Charger le .env du dossier backend
dotenv_path = os.path.join(os.path.dirname(__file__), "..", "backend", ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Importer Base et modèles
from backend.database import Base
import backend.models  # <-- Charge tous les modèles déclarés dans backend/models/__init__.py

# Config Alembic
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# Construire DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME")
    if not all([DB_USER, DB_PASS, DB_NAME]):
        raise Exception("Variables d'environnement DB manquantes dans .env")
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

config.set_main_option("sqlalchemy.url", DATABASE_URL)


def run_migrations_offline() -> None:
    """Exécuter les migrations en mode offline (SQL brut sans connexion)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Exécuter les migrations en mode online (connexion DB)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
