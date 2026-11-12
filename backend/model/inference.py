import torch
from torchvision import transforms, models
from PIL import Image
import os

# ======== Config ========
MODEL_PATH = "backend/model/train_plant_disease_model.pt"
CLASS_NAMES = ["maize_disease", "maize_healthy"]  # 🔁 Change si tu ajoutes plus de classes
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ======== Prétraitement ========
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# ======== Charger modèle ========
def load_model():
    model = models.resnet18(pretrained=False)
    model.fc = torch.nn.Linear(model.fc.in_features, len(CLASS_NAMES))
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    model.eval()
    model.to(DEVICE)
    return model

# ======== Inférence ========
def predict_image(image_path):
    image = Image.open(image_path).convert("RGB")
    input_tensor = transform(image).unsqueeze(0).to(DEVICE)

    model = load_model()
    with torch.no_grad():
        output = model(input_tensor)
        _, predicted = torch.max(output, 1)
        return CLASS_NAMES[predicted.item()]

# ======== Test rapide ========
if __name__ == "__main__":
    test_image = "backend/model/test_image.jpg"  # 🔁 Change par ton image
    if not os.path.exists(test_image):
        print("❌ Image de test non trouvée :", test_image)
    else:
        prediction = predict_image(test_image)
        print(f"🧠 Prédiction : {prediction}")
