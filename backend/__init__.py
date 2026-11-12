# backend/__init__.py

from backend.database.base import Base, engine
from backend import models  # Importe tous les modèles regroupés dans models/__init__.py


def init_db():
    """
    Initialise la base de données.
    Toutes les tables des modèles importés dans backend/models seront créées.
    """
    Base.metadata.create_all(bind=engine)
    print("✅ Tables créées avec succès.")


if __name__ == "__main__":
    init_db()
