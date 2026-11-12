import os
import torch
import torchvision
from torchvision import transforms, datasets, models
from torch.utils.data import DataLoader
from torch import nn, optim

# ============ Configuration ============
DATA_DIR = "./dataset"
TRAIN_DIR = os.path.join(DATA_DIR, "train")
VAL_DIR = os.path.join(DATA_DIR, "val")
MODEL_PATH = "backend/model/train_plant_disease_model.pt"
BATCH_SIZE = 16
EPOCHS = 10

# ============ Vérification ============
if not os.path.exists(TRAIN_DIR) or not os.listdir(TRAIN_DIR):
    raise RuntimeError(f"Aucune classe trouvée dans {TRAIN_DIR}. Vérifiez la structure du dataset.")

# Compter les sous-dossiers (classes)
NUM_CLASSES = len([d for d in os.listdir(TRAIN_DIR) if os.path.isdir(os.path.join(TRAIN_DIR, d))])

# Détection GPU
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ============ Prétraitement ============
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

train_data = datasets.ImageFolder(TRAIN_DIR, transform=transform)
val_data = datasets.ImageFolder(VAL_DIR, transform=transform)

train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_data, batch_size=BATCH_SIZE)

# ============ Modèle ============
model = models.resnet18(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, NUM_CLASSES)
model = model.to(DEVICE)

# ============ Entraînement ============
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()

    print(f"📘 Époque {epoch+1}/{EPOCHS}, Perte: {running_loss/len(train_loader):.4f}")

# ============ Sauvegarde ============
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
torch.save(model.state_dict(), MODEL_PATH)
print(f"✅ Modèle sauvegardé dans: {MODEL_PATH}")
