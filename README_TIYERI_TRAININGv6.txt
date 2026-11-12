========================
 Guide d'entraînement IA TIYERI (Maladies des plantes)
========================

1. 📁 Préparation du dataset :
   - Allez dans le dossier 'dataset/'
   - Pour chaque plante (ex: mais/), ajoutez des images dans les sous-dossiers :
     maladies/, carences/, ravageurs/, saines/
   - Format d'image recommandé : JPG ou PNG (640x640 ou 512x512)
   - Exemple : dataset/mais/maladies/rouille_1.jpg

2. ⚙️ Installation des dépendances :
   pip install torch torchvision opencv-python tqdm matplotlib

3. 🚀 Lancement de l'entraînement :
   python model/train.py

4. 🔎 Prédiction (démo) :
   python model/predict.py path/to/image.jpg

5. 🔄 Intégration dans TIYERI IA :
   - Une fois entraîné, intégrez le modèle .pth dans vos scripts d'analyse
   - Utilisez les labels de labels.json pour interpréter les sorties

Bonne chance ! 🌿