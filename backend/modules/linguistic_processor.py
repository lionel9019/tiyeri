import re
import difflib
import unicodedata
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from symspellpy import SymSpell, Verbosity
from transformers import pipeline

# Téléchargement de ressources NLTK si pas déjà fait
nltk.download('punkt')
nltk.download('stopwords')

# Chargement du correcteur SymSpell
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
sym_spell.load_dictionary("backend/data/frequency_dictionary_en_82_765.txt", term_index=0, count_index=1)

# Générateur de phrases
generator = pipeline("text-generation", model="distilgpt2")

# Vocabulaire de base à enrichir avec ton domaine
VOCABULAIRE_TYERI = {
    "engrais", "maladie", "feuille", "culture", "maïs", "arachide", "champ", "pluie",
    "semis", "récolte", "bio", "pesticide", "diagnostic", "traitement", "pH", "sol"
}

STOPWORDS_FR = set(stopwords.words("french"))

def nettoyer_texte(texte: str) -> str:
    texte = texte.lower()
    texte = re.sub(r"[^a-zA-Z0-9\s]", "", texte)
    return texte.strip()

#def nettoyer_texte(texte):
 #   texte = texte.lower()
  #  texte = unicodedata.normalize('NFKD', texte).encode('ASCII', 'ignore').decode('utf-8')
   # texte = re.sub(r"[^a-z0-9\s]", "", texte)
    #return texte

def corriger_texte(texte: str) -> str:
    mots = texte.split()
    corriges = []
    for mot in mots:
        suggestions = sym_spell.lookup(mot, Verbosity.CLOSEST, max_edit_distance=2)
        corriges.append(suggestions[0].term if suggestions else mot)
    return " ".join(corriges)

def detecter_mots_et_fautes(message):
    texte_nettoye = nettoyer_texte(message)
    tokens = word_tokenize(texte_nettoye, language="french")
    mots_utiles = [t for t in tokens if t not in STOPWORDS_FR]
    resultats = []

    for mot in mots_utiles:
        mot_corrige = corriger_mot(mot)
        resultats.append((mot, mot_corrige))

    return resultats

def corriger_mot(mot):
    suggestions = difflib.get_close_matches(mot, VOCABULAIRE_TYERI, n=1, cutoff=0.6)
    return suggestions[0] if suggestions else mot

def generer_phrase(texte: str) -> str:
    try:
        res = generator(texte, max_length=50, num_return_sequences=1)[0]['generated_text']
        return res.strip()
    except Exception as e:
        return f"Erreur génération : {e}"

def generer_phrase_correcte(message):
    mots = detecter_mots_et_fautes(message)
    phrase = " ".join([corrige for original, corrige in mots])
    return phrase.capitalize() + "."

def analyser_et_corriger(message: str) -> str:
    propre = nettoyer_texte(message)
    corrige = corriger_texte(propre)
    phrase = generer_phrase(corrige)
    return phrase
    
# Exemple d’utilisation :
if __name__ == "__main__":
    message = "feileu malade maix"
    print("Phrase corrigée :", generer_phrase_correcte(message))
