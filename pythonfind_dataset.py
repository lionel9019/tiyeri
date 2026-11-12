import os

# Nom du dossier que tu cherches
TARGET = "PlantVillage"

# Point de départ de la recherche (par ex. ton projet)
ROOT_DIR = r"H:\Bureau\IA TIYERI STARTUP\API\IA TIYERI\V9"

print(f"🔍 Recherche de '{TARGET}' dans {ROOT_DIR} ...")

found_paths = []
for root, dirs, files in os.walk(ROOT_DIR):
    if TARGET in dirs:
        path = os.path.join(root, TARGET)
        found_paths.append(path)

if found_paths:
    print("\n✅ Dossier trouvé :")
    for p in found_paths:
        print("   ", os.path.abspath(p))
else:
    print("\n❌ Aucun dossier trouvé, vérifie que tu as bien décompressé ton dataset.")
