import shutil
import os

paths = [
    r"H:\Bureau\IA TIYERI STARTUP\API\IA TIYERI\V9\venv\Lib\site-packages\~umpy",
    r"H:\Bureau\IA TIYERI STARTUP\API\IA TIYERI\V9\venv\Lib\site-packages\~umpy.libs"
]

for path in paths:
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
            print(f"✅ Supprimé : {path}")
        except Exception as e:
            print(f"❌ Impossible de supprimer {path} : {e}")
    else:
        print(f"⚠️ Introuvable : {path}")
