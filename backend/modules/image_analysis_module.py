import io
import os
import base64
from PIL import Image
import numpy as np
import tensorflow as tf

from backend.database.utils import get_diagnostic_response
#from backend.database import SessionLocal  

from backend.database.base import SessionLocal  # ✅ import correct
# === CONFIGURATION ===
MODEL_PATH = "backend/models/plant_disease_model.h5"

LABELS = [
    "Bacterialblight",
    "Brownspot",
    "Leafsmut",
    "Pepper__bell___Bacterial_spot",
    "Pepper__bell___healthy",
    "Potato___Early_blight",
    "Potato___healthy",
    "Potato___Late_blight",
    "Tomato_Bacterial_spot",
    "Tomato_Early_blight",
    "Tomato_healthy",
    "Tomato_Late_blight",
    "Tomato_Leaf_Mold",
    "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite",
    "Tomato__Target_Spot",
    "Tomato__Tomato_mosaic_virus",
    "Tomato__Tomato_YellowLeaf__Curl_Virus"
]


# === CHARGEMENT DU MODÈLE ===
def load_model():
    print("🔄 Chargement du modèle TensorFlow...")
    model = tf.keras.models.load_model(MODEL_PATH)
    print("✅ Modèle chargé avec succès")
    return model

model = load_model()

# === TRANSFORMATION IMAGE ===
def preprocess_image(image: Image.Image) -> np.ndarray:
    image = image.resize((224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(image)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

# === ANALYSE D'IMAGE ===
def analyze_crop_image(file_input):
    """
    Analyse une image (bytes, chemin ou base64).
    """
    try:
        print("🟢 Début de l'analyse d'image")

        # Gestion des différents types d'entrée
        if isinstance(file_input, bytes):
            image = Image.open(io.BytesIO(file_input)).convert("RGB")
        elif isinstance(file_input, str):
            if os.path.exists(file_input):  # chemin local
                image = Image.open(file_input).convert("RGB")
            else:  # string base64
                file_bytes = base64.b64decode(file_input)
                image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
        else:
            raise ValueError("Format de fichier non supporté")

        img_array = preprocess_image(image)

        predictions = model.predict(img_array)
        confidence = float(np.max(predictions))
        predicted_idx = int(np.argmax(predictions, axis=1)[0])
        prediction = LABELS[predicted_idx]

        print(f"📊 Prédiction : {prediction} avec confiance {confidence:.2f}")

        # Confiance trop faible
        if confidence < 0.6:
            return {
                "diagnostic": "Inconnu",
                "description": "L'image ne correspond pas clairement à une plante ou culture agricole connue.",
                "traitement": "Aucun traitement proposé.",
                "conseils": "Vérifiez la qualité de la photo ou consultez un technicien agricole."
            }

        # 🔎 Récupération en base
        db = SessionLocal()
        db_response = get_diagnostic_response(db, prediction)
        db.close()

        if db_response:
            return {
                 "diagnostic": prediction,
        "culture": getattr(db_response, "culture", None),
        "description": getattr(db_response, "description", None),
        "nom_scientifique": getattr(db_response, "nom_scientifique", None),
        "origine": getattr(db_response, "origine", None),
        "sol": getattr(db_response, "sol", None),
        "varietes": getattr(db_response, "varietes", None),
        "rendement": getattr(db_response, "rendement", None),
        "nutrition": getattr(db_response, "nutrition", None),
        "toxicite": getattr(db_response, "toxicite", None),
        "medicinal": getattr(db_response, "medicinal", None),
        "produits": getattr(db_response, "produits", None),
        "saisons": getattr(db_response, "saisons", None),
        "traitement": getattr(db_response, "traitement", None),
        "conseils": getattr(db_response, "conseils", None),
        "itineraire": getattr(db_response, "itineraire", None),
        "confiance": confidence
            }
        else:
            return {
                "diagnostic": prediction,
                "description": "Aucune information détaillée trouvée dans la base.",
                "traitement": "Aucun traitement connu.",
                "conseils": "Consultez un technicien agricole pour plus d’informations.",
                "confiance": confidence
            }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"erreur": f"❌ Erreur lors de l'analyse de l'image : {str(e)}"}

# === ANALYSE TEXTE SYMPTÔMES ===
def analyze_crop_symptoms(symptoms_text: str):
    try:
        symptoms_text = symptoms_text.lower()

        if "taches jaunes" in symptoms_text or "feuilles jaunes" in symptoms_text:
            return {
                "diagnostic": "Carence en azote",
                "description": "Les feuilles jaunissent souvent à cause d'un manque d'azote.",
                "traitement": "Apporter un engrais riche en azote.",
                "conseils": "Alterner avec du compost ou du fumier organique."
            }
        elif "taches brunes" in symptoms_text or "feuilles sèches" in symptoms_text:
            return {
                "diagnostic": "Mildiou ou stress hydrique",
                "description": "Les taches brunes peuvent être liées au mildiou ou au manque d’eau.",
                "traitement": "Appliquer un traitement fongicide bio (bouillie bordelaise).",
                "conseils": "Améliorer l’irrigation et espacer les plants."
            }
        else:
            return {
                "diagnostic": "Inconnu",
                "description": "Les symptômes ne correspondent pas à une maladie connue.",
                "traitement": "Consultez un technicien agricole pour confirmation.",
                "conseils": "Fournissez plus de détails (culture, sol, climat...)."
            }
    except Exception as e:
        return {"erreur": f"❌ Erreur lors de l'analyse des symptômes : {str(e)}"}
