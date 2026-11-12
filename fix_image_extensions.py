import os

train_dir = "./dataset/train"

for class_dir in os.listdir(train_dir):
    class_path = os.path.join(train_dir, class_dir)
    for filename in os.listdir(class_path):
        file_path = os.path.join(class_path, filename)
        # Convertir .JPG en .jpg
        if filename.endswith(".JPG"):
            new_name = filename.replace(".JPG", ".jpg")
            os.rename(file_path, os.path.join(class_path, new_name))
            print(f"🔁 Renommé : {filename} -> {new_name}")
        # Corriger double extension
        elif ".jpg.png" in filename:
            new_name = filename.replace(".jpg.png", ".jpg")
            os.rename(file_path, os.path.join(class_path, new_name))
            print(f"🔁 Corrigé double extension : {filename} -> {new_name}")
