import json
import os
import re
import mysql.connector
from mysql.connector import Error
from langdetect import detect
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
from transformers import pipeline
from backend.modules.image_analysis_module import analyze_crop_symptoms, analyze_crop_image
from backend.modules.wikipedia_search import search_wikipedia  # Ajouté pour recherche Web

# ===================== Chargement modèle NLP =====================
try:
    reformulate = pipeline("text2text-generation", model="google/flan-t5-base")
except Exception as e:
    reformulate = None
    print("[ERREUR] Chargement du modèle linguistique échoué:", e)

# ===================== Configuration =====================
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASS", ""),
    "database": os.getenv("DB_NAME", "tiyeri_v2"),
    "port": int(os.getenv("DB_PORT", 3306))
}

DATA_FILE = "chat_memory.json"
RESOURCE_FILE = "agri_resources.json"


def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


chat_memory = load_json(DATA_FILE)
agri_resources = load_json(RESOURCE_FILE)

# ===================== Connexion MySQL =====================
def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print("[ERREUR] Connexion DB:", e)
    return None


# ===================== Chargement des intentions =====================
def get_intents_from_db(lang="fr"):
    conn = get_connection()
    if conn is None:
        return []
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT intent, phrase, response FROM chatbot_intents WHERE langue = %s", (lang,))
            return cursor.fetchall()
    except Exception as e:
        print("[ERREUR] Lecture intentions DB:", e)
        return []
    finally:
        conn.close()


# ===================== Traduction =====================
def detect_language(text):
    try:
        lang = detect(text)
        return lang if lang in ["fr", "en"] else "fr"
    except:
        return "fr"


def translate(text, source, target):
    if source == target:
        return text
    try:
        return GoogleTranslator(source=source, target=target).translate(text)
    except Exception as e:
        print("[ERREUR] Traduction:", e)
        return text


# ===================== Réécriture linguistique =====================
def corriger_et_reformuler(message):
    if not reformulate:
        return message
    try:
        correction = reformulate(f"Reformule cette phrase correctement: {message}", max_new_tokens=128)[0]['generated_text']
        return correction
    except Exception as e:
        print("[ERREUR] Reformulation:", e)
        return message


# ===================== Analyse de composition =====================
def analyse_linguistique(text):
    lettres = re.findall(r"[a-zA-Z]", text)
    chiffres = re.findall(r"\d", text)
    mots = re.findall(r"\b\w+\b", text)
    return {
        "lettres": lettres,
        "chiffres": chiffres,
        "mots": mots,
        "nb_lettres": len(lettres),
        "nb_chiffres": len(chiffres),
        "nb_mots": len(mots)
    }


# ===================== Correspondance avec intentions =====================
def match_intent_and_respond(text, lang="fr"):
    intents = get_intents_from_db(lang)
    text_lower = text.lower()
    for item in intents:
        phrases = [p.strip() for p in item['phrase'].split(',')]
        for p in phrases:
            if p and p in text_lower:
                return item['response']
    return None

# ===================== Traitement principal =====================
def process_user_message(message, lang="fr"):
    original_text = message.strip()
    texte_corrige = original_text
    texte_fr = texte_corrige if lang == "fr" else translate(texte_corrige, lang, "fr")

    print("[Original]", original_text)
    print("[Langue préférée]", lang)
    print("[Texte pour recherche]", texte_fr)

    if texte_fr.lower() in chat_memory:
        reponse = chat_memory[texte_fr.lower()]
        return reponse if lang == "fr" else translate(reponse, "fr", lang)

    reponse_db = match_intent_and_respond(texte_fr, lang="fr")
    if reponse_db:
        return reponse_db if lang == "fr" else translate(reponse_db, "fr", lang)

    try:
        web_result = search_wikipedia(texte_fr)
        if web_result:
            return web_result if lang == "fr" else translate(web_result, "fr", lang)
    except Exception as e:
        print("[ERREUR] Recherche Wikipedia:", e)

    return "🤖 Je n'ai pas compris. Pouvez-vous reformuler ?" if lang == "fr" else "🤖 I didn't understand. Could you rephrase?"


