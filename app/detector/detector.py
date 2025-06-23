import os
import tempfile
from gradio_client import Client, handle_file
from fastapi import HTTPException
from dotenv import load_dotenv
import logging

load_dotenv()

HF_SPACE_NAME = "pebipebriansah16/deteksi-penyakit-cabai"
HF_TOKEN = os.getenv("HF_TOKEN")

client = Client(HF_SPACE_NAME, hf_token=HF_TOKEN)

def parse_result_text(text: str) -> dict:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    
    if not lines:
        return {"label": None, "confidences": []}
    
    label = lines[0]  # Label utama

    confidences = []
    for i in range(1, len(lines), 2):
        try:
            lbl = lines[i]
            confidence_str = lines[i + 1].replace('%', '')
            confidence = float(confidence_str) / 100.0
            confidences.append({"label": lbl.capitalize(), "confidence": round(confidence, 4)})
        except (IndexError, ValueError):
            continue  # Skip error entry
    
    return {"label": label.capitalize(), "confidences": confidences}

async def predict_disease(image_bytes: bytes) -> dict:
    temp_file_path = None
    try:
        # Simpan file gambar sementara
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(image_bytes)
            temp_file_path = temp_file.name

        # Kirim gambar ke endpoint Gradio / Hugging Face
        result = client.predict(
            image=handle_file(temp_file_path),
            api_name="/predict"
        )

        # Logging (opsional)
        logging.info(f"Model response: {result}")

        # Validasi format response
        if not isinstance(result, dict) or "label" not in result or "confidences" not in result:
            raise HTTPException(status_code=500, detail="Format response model tidak valid.")

        # Langsung kembalikan result sebagai 'data'
        return {"data": result}

    except Exception as e:
        logging.exception("Prediction failed")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
