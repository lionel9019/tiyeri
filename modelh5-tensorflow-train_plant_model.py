import os
from tf_keras.preprocessing.image import ImageDataGenerator
from tf_keras.models import Model
from tf_keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tf_keras.applications import MobileNetV2
import tensorflow as tf

# 📂 Utiliser le bon dataset (⚠️ vérifie ton chemin exact)
DATASET_DIR = r"H:\Bureau\IA TIYERI STARTUP\API\IA TIYERI\V9\dataset\PlantVillage"
IMG_SIZE = (224, 224)
BATCH_SIZE = 16

# 🔄 Data augmentation
datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    validation_split=0.2,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True
)

print("🔎 Vérification dataset...")
print("Chemin défini :", DATASET_DIR)
print("Existe ?", os.path.exists(DATASET_DIR))
print("Contenu :", os.listdir(DATASET_DIR) if os.path.exists(DATASET_DIR) else "❌ Introuvable")

# 🏋️ Générateurs
train_gen = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    subset="training"
)

val_gen = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    subset="validation"
)

# ✅ Charger MobileNetV2 pré-entraîné
base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False  # geler au début

# 🔗 Ajouter nos couches custom
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.3)(x)
preds = Dense(train_gen.num_classes, activation="softmax")(x)

model = Model(inputs=base_model.input, outputs=preds)

# ⚙️ Compiler
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# 🚀 Entraînement rapide (5 époques seulement pour test)
history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=5
)

# 💾 Sauvegarde modèle
os.makedirs("backend/models", exist_ok=True)
model.save("backend/models/plant_disease_model.h5")

print("✅ Modèle test rapide entraîné et sauvegardé !")
