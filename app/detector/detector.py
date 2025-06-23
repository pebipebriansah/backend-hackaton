import os
import tempfile
from gradio_client import Client, handle_file
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

HF_SPACE_NAME = "pebipebriansah16/deteksi-penyakit-cabai"
HF_TOKEN = os.getenv("HF_TOKEN")

client = Client(HF_SPACE_NAME, hf_token=HF_TOKEN)

async def predict_disease(image_bytes: bytes) -> dict:
    import logging
    temp_file_path = None
    try:
        # Simpan file gambar sementara
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(image_bytes)
            temp_file_path = temp_file.name

        # Kirim ke Gradio
        result = client.predict(
            image=handle_file(temp_file_path),
            api_name="/predict"
        )

        # Debug untuk memastikan format
        if not isinstance(result, dict):
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected result format: {type(result)} - value: {result}"
            )

        # Konversi ke format yang diminta frontend Flutter
        confidences = []
        for k, v in result.items():
            # Pastikan confidence adalah float
            try:
                confidences.append({
                    "label": str(k),
                    "confidence": float(v)
                })
            except Exception:
                continue  # skip jika tidak bisa dikonversi

        if not confidences:
            raise HTTPException(status_code=500, detail="Tidak ada label valid dari model.")

        # Ambil label dengan confidence tertinggi
        top_label = max(confidences, key=lambda x: x['confidence'])['label']

        return {
            "data": {
                "label": top_label,
                "confidences": confidences
            }
        }

    except Exception as e:
        logging.exception("Prediction failed")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)

