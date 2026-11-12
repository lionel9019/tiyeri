# backend/train/train_model.py

import os
import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from tqdm import tqdm

# === CONFIGURATION ===
DATA_DIR = "dataset"
BATCH_SIZE = 32
EPOCHS = 10
MODEL_PATH = "backend/model/train_plant_disease_model.pt"

# === PRÉTRAITEMENT ===
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# === DONNÉES ===
train_data = datasets.ImageFolder(os.path.join(DATA_DIR, "train"), transform=transform)
val_data = datasets.ImageFolder(os.path.join(DATA_DIR, "val"), transform=transform)

train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_data, batch_size=BATCH_SIZE)

# === MODÈLE ===
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = models.resnet18(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, len(train_data.classes))  # 🔁 nombre automatique
model = model.to(device)

# === OPTIMISATION ===
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# === ENTRAÎNEMENT ===
for epoch in range(EPOCHS):
    model.train()
    total_loss = 0
    for images, labels in tqdm(train_loader, desc=f"Époque {epoch+1}/{EPOCHS}"):
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f"[{epoch+1}] Perte moyenne : {total_loss / len(train_loader):.4f}")

# === ÉVALUATION ===
model.eval()
correct = total = 0
with torch.no_grad():
    for images, labels in val_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        _, preds = torch.max(outputs, 1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)

print(f"✅ Précision sur validation : {correct/total*100:.2f}%")

# === SAUVEGARDE ===
torch.save(model.state_dict(), MODEL_PATH)
print("📦 Modèle sauvegardé avec succès à :", MODEL_PATH)

# === SAUVEGARDE DES ÉTIQUETTES ===
with open("backend/model/labels.txt", "w", encoding="utf-8") as f:
    for label in train_data.classes:
        f.write(label + "\n")
