import os

# Set backend JAX harus dilakukan **sebelum** import keras
os.environ["KERAS_BACKEND"] = "jax"

from huggingface_hub import login
import keras
import numpy as np
from PIL import Image
import io

# Login ke Hugging Face dengan token dari environment variable
token = os.environ.get("HF_TOKEN")
if token:
    login(token)

# Load model dari Hugging Face sekali saja saat import module
model = keras.saving.load_model("hf://pebipebriansah16/deteksi-cabai")

# Mapping label kelas
class_names = ["thrips", "virus_kuning", "bercak_daun"]

def predict_disease(image_bytes: bytes) -> dict:
    # Load gambar dari bytes, ubah ke RGB dan resize sesuai model
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((224, 224))

    # Preprocess: ubah ke numpy array dan normalisasi
    image_array = np.array(image) / 255.0

    # Tambah batch dimension: (1, 224, 224, 3)
    image_array = np.expand_dims(image_array, axis=0)

    # Prediksi menggunakan model Keras
    prediction = model.predict(image_array)

    # Ambil kelas dengan probabilitas tertinggi
    predicted_class = int(np.argmax(prediction, axis=1)[0])
    confidence = float(np.max(prediction))

    return {
        "class": class_names[predicted_class],
        "confidence": confidence
    }
