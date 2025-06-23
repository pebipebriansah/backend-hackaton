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
    temp_file_path = None
    try:
        # Simpan file gambar sementara
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(image_bytes)
            temp_file_path = temp_file.name

        # Kirim ke Gradio endpoint (asumsi `predict` adalah route utama)
        result = client.predict(
            image=handle_file(temp_file_path),
            api_name="/predict"  # pastikan sesuai dengan `gr.Interface(fn=..., api_name="/predict")` jika ingin eksplisit
        )

        # Output sudah berupa dictionary hasil prediksi (confidence setiap label)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
