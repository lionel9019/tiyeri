import os
from PIL import Image, ImageDraw
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

# ==== 1. Génération dataset ====

def create_leaf_image(color, spots=None, save_path=None):
    img = Image.new("RGB", (128, 128), color)
    draw = ImageDraw.Draw(img)
    if spots:
        for spot in spots:
            x, y, r, c = spot
            draw.ellipse((x - r, y - r, x + r, y + r), fill=c)
    if save_path:
        img.save(save_path)

def generate_dataset(base_dir="dataset_demo"):
    classes = {
        "healthy": [(34, 139, 34)],
        "disease_spot": [(34, 139, 34), (80, 80, 20, (255, 0, 0))],
        "disease_yellow": [(34, 139, 34), (60, 60, 25, (255, 255, 0))]
    }
    for split in ["train", "val"]:
        for cls, val in classes.items():
            dir_path = os.path.join(base_dir, split, cls)
            os.makedirs(dir_path, exist_ok=True)
            count = 10 if split == "train" else 3
            for i in range(count):
                if cls == "healthy":
                    color = val[0]
                    create_leaf_image(color, save_path=os.path.join(dir_path, f"{cls}_{i}.png"))
                else:
                    bg = val[0]
                    spot = val[1]
                    create_leaf_image(bg, spots=[spot], save_path=os.path.join(dir_path, f"{cls}_{i}.png"))

# ==== 2. Entraînement modèle ====

def train_model():
    DATA_DIR = "./dataset_demo"
    MODEL_SAVE_PATH = "./backend/madel/plant_disease_model.pt"
    BATCH_SIZE = 4
    NUM_CLASSES = 3
    EPOCHS = 5
    LEARNING_RATE = 0.001

    transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ])

    train_dataset = datasets.ImageFolder(os.path.join(DATA_DIR, "train"), transform=transform)
    val_dataset = datasets.ImageFolder(os.path.join(DATA_DIR, "val"), transform=transform)

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

    model = models.resnet18(pretrained=True)
    model.fc = nn.Linear(model.fc.in_features, NUM_CLASSES)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    for epoch in range(EPOCHS):
        model.train()
        running_loss = 0.0
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        print(f"Epoch {epoch+1}/{EPOCHS} - Loss: {running_loss/len(train_loader):.4f}")

        # Validation
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                correct += (preds == labels).sum().item()
                total += labels.size(0)
        print(f"Validation Accuracy: {correct / total:.2%}")

    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    torch.save(model.state_dict(), MODEL_SAVE_PATH)
    print(f"Modèle sauvegardé sous {MODEL_SAVE_PATH}")

# ==== Main ====

if __name__ == "__main__":
    print("Génération du mini dataset...")
    generate_dataset()
    print("Entraînement du modèle...")
    train_model()
