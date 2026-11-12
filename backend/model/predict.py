# predict.py : Prédiction avec le modèle TIYERI IA
import sys, json, torch
from torchvision import models, transforms
from PIL import Image

img_path = sys.argv[1]
model = models.resnet18()
model.fc = torch.nn.Linear(model.fc.in_features, 16)
model.load_state_dict(torch.load("tiyeri_model.pth"))
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])
img = Image.open(img_path).convert("RGB")
img_tensor = transform(img).unsqueeze(0)
with open("labels.json") as f:
    labels = json.load(f)
output = model(img_tensor)
_, predicted = torch.max(output, 1)
print("✅ Classe prédite :", labels[predicted.item()])