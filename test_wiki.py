import wikipedia

# Configurer la langue en français
wikipedia.set_lang("fr")

# Exemple de recherche
requete = input("🔍 Entrez un sujet à rechercher : ")

try:
    resume = wikipedia.summary(requete, sentences=2)
    print(f"\n📘 Résumé Wikipédia pour « {requete} » :\n{resume}")
except wikipedia.exceptions.DisambiguationError as e:
    print("⚠️ Plusieurs sujets trouvés :")
    for option in e.options[:5]:
        print(f" - {option}")
except wikipedia.exceptions.PageError:
    print("❌ Aucun résultat trouvé.")
except Exception as ex:
    print(f"🚨 Erreur : {ex}")
