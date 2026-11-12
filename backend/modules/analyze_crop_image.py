import os
import torch
from torchvision import models, transforms
from PIL import Image

# ============ Chemins ============
MODEL_PATH = "backend/model/train_plant_disease_model.pt"
LABELS_PATH = "backend/model/class_labels.txt"

# ============ Dispositif ============
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ============ Prétraitement ============
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# ============ Chargement des classes ============
def load_class_labels(path=LABELS_PATH):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]

CLASS_LABELS = load_class_labels()

# ============ Chargement du modèle ============
def load_model(path=MODEL_PATH):
    model = models.resnet18(pretrained=False)
    model.fc = torch.nn.Linear(model.fc.in_features, len(CLASS_LABELS))
    model.load_state_dict(torch.load(path, map_location=DEVICE))
    model.to(DEVICE)
    model.eval()
    return model

MODEL = load_model()

# ============ Fonction d’analyse ============
def analyze_crop_image(image_path: str) -> dict:
    try:
        image = Image.open(image_path).convert("RGB")
        input_tensor = transform(image).unsqueeze(0).to(DEVICE)
        with torch.no_grad():
            outputs = MODEL(input_tensor)
            _, predicted = torch.max(outputs, 1)
            predicted_label = CLASS_LABELS[predicted.item()]
        return {
            "status": "ok",
            "prediction": predicted_label
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
