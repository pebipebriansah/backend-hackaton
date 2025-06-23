import os
import tempfile
import logging
from fastapi import HTTPException
from gradio_client import Client, handle_file
from dotenv import load_dotenv

load_dotenv()

HF_SPACE_NAME = "pebipebriansah16/deteksi-penyakit-cabai"
HF_TOKEN = os.getenv("HF_TOKEN")

client = Client(HF_SPACE_NAME, hf_token=HF_TOKEN)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)


async def predict_disease(image_bytes: bytes, max_retries: int = 3) -> dict:
    """
    Kirim gambar ke Hugging Face Space dan dapatkan prediksi.
    Gunakan file sementara karena gradio_client memerlukan handle_file().
    """
    attempt = 0
    last_exception = None
    temp_file_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(image_bytes)
            temp_file_path = temp_file.name

        while attempt < max_retries:
            try:
                logging.info(f"[Attempt {attempt + 1}] Sending to HF: {temp_file_path}")
                result = client.predict(
                    image=handle_file(temp_file_path),
                    api_name="/predict"
                )

                # Validasi format
                if isinstance(result, dict) and "label" in result and "confidences" in result:
                    logging.info(f"Prediction result: {result}")
                    return {"data": result}

                raise ValueError("Response format tidak sesuai")

            except Exception as e:
                logging.warning(f"Prediction attempt {attempt + 1} failed: {e}")
                last_exception = e
                attempt += 1

        logging.error("All prediction attempts failed.")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {last_exception}")

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
