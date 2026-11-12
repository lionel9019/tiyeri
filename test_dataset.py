import os

TRAIN_DIR = "./dataset/train"

if not os.path.exists(TRAIN_DIR):
    print("❌ Dossier 'dataset/train' introuvable.")
    exit()

print(f"📁 Vérification du contenu de : {TRAIN_DIR}")
for class_dir in os.listdir(TRAIN_DIR):
    class_path = os.path.join(TRAIN_DIR, class_dir)
    print(f"🔎 Classe : {class_dir}")
    if os.path.isdir(class_path):
        files = os.listdir(class_path)
        for file in files:
            print(f"   └── {file}")
    else:
        print("   ⚠️ Ce n’est pas un dossier de classe.")
