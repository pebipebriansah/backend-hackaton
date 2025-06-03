import os
import httpx
from fastapi import FastAPI, File, UploadFile, HTTPException

app = FastAPI()

# URL inference API Hugging Face (ganti sesuai repo dan model kamu)
HF_API_URL = "https://api-inference.huggingface.co/models/pebipebriansah16/deteksi-cabai"
HF_TOKEN = os.getenv("HF_TOKEN")

headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not HF_TOKEN:
        raise HTTPException(status_code=500, detail="HF_TOKEN environment variable is not set")

    image_bytes = await file.read()

    async with httpx.AsyncClient() as client:
        response = await client.post(
            HF_API_URL,
            headers=headers,
            files={"file": (file.filename, image_bytes, file.content_type)}
        )
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"Hugging Face API error: {response.text}")

    result = response.json()
    # Result tergantung output model kamu, sesuaikan parsing di sini
    return {"result": result}
