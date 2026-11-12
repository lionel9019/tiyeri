# train.py : Entraînement d'un modèle simple ResNet18 pour TIYERI IA
import os, json, torch
from torchvision import datasets, transforms, models
from torch import nn, optim
from torch.utils.data import DataLoader

data_dir = '../dataset'
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

dataset = datasets.ImageFolder(data_dir, transform=transform)
loader = DataLoader(dataset, batch_size=32, shuffle=True)
model = models.resnet18(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, len(dataset.classes))
model.to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(10):
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        output = model(images)
        loss = criterion(output, labels)
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch+1} terminé - Loss: {loss.item()}")

torch.save(model.state_dict(), "tiyeri_model.pth")
with open("labels.json", "w") as f:
    json.dump(dataset.classes, f)