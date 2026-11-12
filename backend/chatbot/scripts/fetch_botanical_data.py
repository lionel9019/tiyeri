import requests
import os
from tqdm import tqdm
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from models import ChatbotIntent  # ta table
from database import SessionLocal  # ta session DB

# Dossier des images
IMAGE_FOLDER = "frontend/images"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Exemple d’API publique (fictive ici)
API_ENDPOINT = "https://api.gbif.org/v1/species/search?q=plant&limit=50"

# Fonction principale
def fetch_and_store_plants():
    db: Session = SessionLocal()

    print("Connexion à l’API en cours…")
    response = requests.get(API_ENDPOINT)
    data = response.json()

    print("Traitement des plantes…")
    for item in tqdm(data.get("results", []), desc="Téléchargement plantes"):
        try:
            # Simulation de données botaniques
            scientific_name = item.get("scientificName")
            usage = "Usage médicinal ou alimentaire (exemple)"  # À remplacer par analyse réelle
            npk = "3-1-4"  # Par défaut ou à analyser
            comestible = "Oui" if "edible" in item.get("vernacularName", "").lower() else "Non"

            # Téléchargement de l'image (exemple)
            image_url = "https://source.unsplash.com/400x400/?plant"  # À remplacer par vraie URL si disponible
            image_name = f"{scientific_name.replace(' ', '_')}.jpg"
            image_path = os.path.join(IMAGE_FOLDER, image_name)

            with open(image_path, "wb") as f:
                img_data = requests.get(image_url).content
                f.write(img_data)

            # Création d’une intention (à adapter selon ton IA TIYERI)
            intent = ChatbotIntent(
                intent=f"plant_{scientific_name.lower().replace(' ', '_')}",
                question=f"Dis-moi ce que tu sais sur la plante {scientific_name} ?",
                response=f"La plante {scientific_name} est utilisée pour : {usage}. Rapport NPK : {npk}. Comestible : {comestible}.",
                image=image_name,
                npk=npk,
                comestible=comestible
            )
            db.add(intent)
            db.commit()

        except Exception as e:
            print(f"Erreur avec {item.get('scientificName')}: {e}")
            continue

    db.close()
    print("✅ Toutes les plantes ont été enregistrées.")

if __name__ == "__main__":
    fetch_and_store_plants()
