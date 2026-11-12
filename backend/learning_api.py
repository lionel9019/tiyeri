from fastapi import APIRouter
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
import sys  

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer


# Charger les variables d'environnement
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(dotenv_path)

# Ajouter le dossier parent au path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

router = APIRouter()
load_dotenv()



# Dossiers utiles
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploaded_docs")
os.makedirs(UPLOAD_DIR, exist_ok=True)
KNOWLEDGE_FILE = os.path.join(os.path.dirname(__file__), "knowledge_base.txt")
CHAT_MEMORY_FILE = os.path.join(os.path.dirname(__file__), "chat_memory.json")

# Configuration JWT
DB_USER = os.getenv("DB_USER")
SECRET_KEY = os.getenv("SECRET_KEY", "ton_secret_très_long_et_complexe_ici")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth3_scheme = OAuth2PasswordBearer(tokenUrl="admin/token")


# Configuration de la connexion MySQL à partir du .env
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASS", ""),
    "database": os.getenv("DB_NAME", "tiyeri_v2"),
    "port": int(os.getenv("DB_PORT", 3306))
}

def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Exception as e:
        print(f"[ERREUR] Connexion DB impossible : {e}")
    return None

# 📥 Récupérer les phrases apprises (non encore validées)
@router.get("/admin/learned-phrases")
def get_learned_phrases():
    conn = get_connection()
    if conn is None:
        return {"error": "Connexion à la base impossible."}
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, phrase, intent, langue, statut FROM chatbot_learnings WHERE statut = 'pending'")
            results = cursor.fetchall()
            return [
                {
                    "id": row[0],
                    "phrase": row[1],
                    "intent": row[2],
                    "langue": row[3],
                    "statut": row[4]
                }
                for row in results
            ]
    except Error as e:
        return {"error": f"Erreur MySQL : {str(e)}"}
    finally:
        conn.close()

# ✅ Valider une phrase (ajouter à chatbot_intents)
@router.post("/admin/validate-phrase/{id}")
def validate_phrase(id: int):
    conn = get_connection()
    if conn is None:
        return {"error": "Connexion à la base impossible."}
    try:
        with conn.cursor() as cursor:
            # Récupérer la phrase
            cursor.execute("SELECT phrase, intent, langue FROM chatbot_learnings WHERE id = %s", (id,))
            row = cursor.fetchone()
            if not row:
                return {"error": "Phrase introuvable"}

            # Insérer dans chatbot_intents
            cursor.execute(
                "INSERT INTO chatbot_intents (phrase, intent, langue) VALUES (%s, %s, %s)",
                (row[0], row[1], row[2])
            )

            # Mettre à jour le statut
            cursor.execute(
                "UPDATE chatbot_learnings SET statut = 'validated' WHERE id = %s",
                (id,)
            )

            conn.commit()
            return {"message": "✅ Phrase validée avec succès."}
    except Error as e:
        return {"error": f"Erreur MySQL : {str(e)}"}
    finally:
        conn.close()

# ❌ Rejeter une phrase
@router.post("/admin/reject-phrase/{id}")
def reject_phrase(id: int):
    conn = get_connection()
    if conn is None:
        return {"error": "Connexion à la base impossible."}
    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE chatbot_learnings SET statut = 'rejected' WHERE id = %s", (id,))
            conn.commit()
            return {"message": "🚫 Phrase rejetée."}
    except Error as e:
        return {"error": f"Erreur MySQL : {str(e)}"}
    finally:
        conn.close()
