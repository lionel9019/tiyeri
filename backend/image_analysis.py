# backend/image_analysis.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
import io
import torch
import torchvision.transforms as transforms

router = APIRouter()

# Exemple de modèle fictif (remplacer par un vrai modèle entraîné)
class DummyModel:
    def predict(self, image_tensor):
        # Simulation : détection de carence phosphore si image sombre/rougeâtre
        return "Carence en phosphore (rougissement, croissance ralentie)"

model = DummyModel()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

@router.post("/diagnostic/image")
def diagnose_image(file: UploadFile = File(...)):
    try:
        image = Image.open(io.BytesIO(file.file.read()))
        image_tensor = transform(image).unsqueeze(0)  # [1, C, H, W]
        prediction = model.predict(image_tensor)
        return {"diagnostic": prediction, "recommandation": "Appliquez un engrais riche en phosphore comme le compost de fumier"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors du traitement de l'image: {str(e)}")
