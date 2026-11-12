import torch
from torchvision import models, transforms
from PIL import Image

LABELS = [
    "Maladie du charbon du maïs",
    "Taches brunes (maladie fongique)",
    "Carence en azote",
    "Flétrissement (manque d'eau)",
    "Feuilles déformées (ravageur)",
    "Sain (aucune anomalie visible)"
]

model = models.resnet18(weights=None)
model.fc = torch.nn.Linear(model.fc.in_features, 6)
model.load_state_dict(torch.load("backend/model/train_plant_disease_model.pt", map_location="cpu"))
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# ⚠️ Chemin vers l'image de test (mets le bon chemin réel ici)
image_path = "mon_image_de_test.jpg"

try:
    image = Image.open(image_path).convert("RGB")
    tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(tensor)
        idx = torch.argmax(output, dim=1).item()
        print("✅ Diagnostic prédit :", LABELS[idx])
except Exception as e:
    print("❌ Erreur lors du test :", str(e))
