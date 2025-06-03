import os

# Set backend JAX sebelum import keras
os.environ["KERAS_BACKEND"] = "jax"

from huggingface_hub import login, hf_hub_download
import keras
import numpy as np
from PIL import Image
import io

# Login ke Hugging Face dengan token (jika disediakan)
token = os.environ.get("HF_TOKEN")
if token:
    login(token)

# Unduh model dari Hugging Face hanya sekali, cache otomatis
model_path = hf_hub_download(
    repo_id="pebipebriansah16/deteksi-cabai",
    filename="Modelpenyakitcabai.keras"  # Ganti dengan nama file model Anda
)

# Load model hanya sekali saat modul pertama kali dijalankan
model = keras.models.load_model(model_path)

# Mapping label kelas
class_names = ["thrips", "virus_kuning", "bercak_daun"]

def predict_disease(image_bytes: bytes) -> dict:
    # Baca gambar dari bytes, ubah ke RGBA (4 channel), resize
    image = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    image = image.resize((224, 224))

    # Preprocessing: ubah ke array dan normalisasi
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)  # Tambah batch dimensi

    # Prediksi
    prediction = model.predict(image_array)
    predicted_class = int(np.argmax(prediction, axis=1)[0])
    confidence = float(np.max(prediction))

    return {
        "class": class_names[predicted_class],
        "confidence": confidence
    }

