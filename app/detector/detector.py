import os
import tempfile
import logging
from fastapi import HTTPException
from gradio_client import Client, handle_file
from dotenv import load_dotenv

# Load environment
load_dotenv()

HF_SPACE_NAME = "pebipebriansah16/deteksi-penyakit-cabai"
HF_TOKEN = os.getenv("HF_TOKEN")

# Setup client & logging
client = Client(HF_SPACE_NAME, hf_token=HF_TOKEN)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)

async def predict_disease(image_bytes: bytes, max_retries: int = 3) -> dict:
    """
    Kirim gambar ke Hugging Face Space dan dapatkan hasil prediksi.
    Gunakan file sementara karena gradio_client memerlukan handle_file().
    """
    temp_file_path = None
    last_exception = None

    try:
        # Simpan gambar ke file sementara
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(image_bytes)
            temp_file_path = temp_file.name

        # Coba beberapa kali jika gagal
        for attempt in range(1, max_retries + 1):
            try:
                logging.info(f"[Attempt {attempt}] Sending image to Hugging Face...")

                # Kirim gambar ke model
                result = client.predict(
                    image=handle_file(temp_file_path),
                    api_name="/predict"
                )

                # Validasi struktur hasil
                if not isinstance(result, dict):
                    raise ValueError("Hasil prediksi bukan dictionary")

                if "label" not in result or "confidences" not in result:
                    raise ValueError("Response tidak mengandung 'label' dan 'confidences'")

                logging.info(f"[Attempt {attempt}] Prediction result: {result}")
                return result  # ✅ Kembalikan langsung tanpa bungkus

            except Exception as e:
                logging.warning(f"[Attempt {attempt}] Prediction failed: {e}")
                last_exception = e

        # Gagal semua percobaan
        logging.error("Semua percobaan prediksi gagal.")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {last_exception}")

    finally:
        # Bersihkan file sementara
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
