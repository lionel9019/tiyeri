from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv
import os

# Charger les variables d'environnement (.env)
load_dotenv()
 
#SECRET_KEY=Admin_90919_@biop2025
#DATABASE_URL=mysql+mysqlconnector://root:root@localhost:3306/tiyeri_v2
# .env
 

DB_USER = "root"
DB_PASSWORD = "tiyeriAdmin2025kdi"
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "tiyeri_v2"

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Créer la connexion
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Inspecter la table
inspector = inspect(engine)

print("📌 Base connectée :", DB_NAME)
print("📌 Tables disponibles :", inspector.get_table_names())

if "diagnostic_responses" in inspector.get_table_names():
    print("\n✅ Colonnes de diagnostic_responses :")
    for column in inspector.get_columns("diagnostic_responses"):
        print(f" - {column['name']} ({column['type']})")
else:
    print("\n❌ La table diagnostic_responses n'existe pas dans cette base.")
