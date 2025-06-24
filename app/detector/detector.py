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
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(image_bytes)
            temp_file_path = temp_file.name

        for attempt in range(1, max_retries + 1):
            try:
                logging.info(f"[Attempt {attempt}] Sending image to Hugging Face...")

                result = client.predict(
                    image=handle_file(temp_file_path),
                    api_name="/predict"
                )

                # 🔍 Tangani jika nested di dalam "data"
                if isinstance(result, dict):
                    if "data" in result and isinstance(result["data"], dict):
                        result = result["data"]

                    if "label" in result and "confidences" in result:
                        logging.info(f"[Attempt {attempt}] Prediction result: {result}")
                        return result  # ✅ return bersih

                raise ValueError("Response format tidak valid")

            except Exception as e:
                logging.warning(f"[Attempt {attempt}] Prediction failed: {e}")
                last_exception = e

        logging.error("Semua percobaan prediksi gagal.")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {last_exception}")

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
