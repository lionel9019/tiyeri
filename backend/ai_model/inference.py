
import shutil
from PIL import Image
from pathlib import Path

async def analyze_image(file):
    dest = Path("static/uploads") / file.filename
    with open(dest, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # IA mock : à remplacer par modèle réel
    if "tache" in file.filename.lower():
        return "Présence de tâches foliaires détectée - suspicion d'alternariose."
    elif "chlorose" in file.filename.lower():
        return "Chlorose détectée - carence probable en azote ou fer."
    return "Analyse effectuée : aucune anomalie flagrante détectée."