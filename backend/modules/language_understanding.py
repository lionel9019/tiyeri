import spacy

# Charger le modèle français
nlp = spacy.load("fr_core_news_md")

def analyser_phrase_utilisateur(phrase):
    doc = nlp(phrase)
    resultats = {
        "mots": [token.text for token in doc],
        "noms": [token.text for token in doc if token.pos_ == "NOUN"],
        "verbes": [token.text for token in doc if token.pos_ == "VERB"],
        "adjectifs": [token.text for token in doc if token.pos_ == "ADJ"],
        "entités": [(ent.text, ent.label_) for ent in doc.ents],
        "longueur_phrase": len(doc)
    }
    return resultats

def generer_phrase(depuis_mots):
    """Génère une phrase simple à partir d’un ensemble de mots"""
    if "nom" in depuis_mots and "verbe" in depuis_mots:
        sujet = depuis_mots.get("nom", "quelqu’un")
        verbe = depuis_mots.get("verbe", "fait")
        return f"{sujet.capitalize()} {verbe} quelque chose."
    return "Je n'ai pas compris, peux-tu reformuler ?"
