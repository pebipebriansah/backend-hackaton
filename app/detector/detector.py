import os
import io
import asyncio
import logging
from gradio_client import Client
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

HF_SPACE_NAME = "pebipebriansah16/deteksi-penyakit-cabai"
HF_TOKEN = os.getenv("HF_TOKEN")

client = Client(HF_SPACE_NAME, hf_token=HF_TOKEN)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
)

def parse_result_text(text: str) -> dict:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return {"label": None, "confidences": []}

    label = lines[0]
    confidences = []
    for i in range(1, len(lines), 2):
        try:
            lbl = lines[i]
            confidence_str = lines[i + 1].replace('%', '')
            confidence = float(confidence_str) / 100.0
            confidences.append({"label": lbl.capitalize(), "confidence": round(confidence, 4)})
        except (IndexError, ValueError):
            continue

    return {"label": label.capitalize(), "confidences": confidences}

async def predict_disease(image_bytes: bytes, max_retries: int = 3) -> dict:
    """
    Kirim gambar ke Hugging Face Space dan dapatkan prediksi.
    Retry otomatis jika gagal sampai max_retries.
    """
    attempt = 0
    last_exception = None

    # Gunakan BytesIO agar tidak perlu simpan file di disk
    image_file = io.BytesIO(image_bytes)
    image_file.name = "image.jpg"  # handle_file butuh attribute name

    while attempt < max_retries:
        try:
            logging.info(f"Predict attempt {attempt + 1}")

            result = client.predict(
                image=image_file,
                api_name="/predict"
            )

            # Reset pointer BytesIO agar bisa dibaca ulang jika retry
            image_file.seek(0)

            # Jika response berupa string, parse dulu
            if isinstance(result, str):
                parsed = parse_result_text(result)
                if parsed["label"] is None:
                    raise ValueError("Parsed label kosong")
                return {"data": parsed}

            # Jika response dict valid, return langsung
            if isinstance(result, dict) and "label" in result and "confidences" in result:
                return {"data": result}

            raise ValueError("Response format tidak valid")

        except Exception as e:
            logging.warning(f"Prediction attempt {attempt + 1} failed: {e}")
            last_exception = e
            attempt += 1
            await asyncio.sleep(1)  # jeda sebelum retry

    # Jika gagal semua retry
    logging.error("Prediction failed after retries")
    raise HTTPException(status_code=500, detail=f"Prediction failed: {last_exception}")

