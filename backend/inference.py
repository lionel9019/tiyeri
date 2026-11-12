import io
from fastapi import UploadFile
from PIL import Image
import tensorflow as tf

# Load a pre-trained MobileNet model
model = tf.keras.applications.mobilenet_v2.MobileNetV2(weights="imagenet")

async def diagnose_image(file: UploadFile):
    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).resize((224,224))
    x = tf.keras.preprocessing.image.img_to_array(img)
    x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
    x = tf.expand_dims(x, 0)
    preds = model.predict(x)
    decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=3)[0]
    return [{"label": label, "description": desc, "score": float(score)} for (label, desc, score) in decoded]