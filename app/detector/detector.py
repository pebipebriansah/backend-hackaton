import os
import httpx
from fastapi import HTTPException

HF_API_URL = "https://api-inference.huggingface.co/models/pebipebriansah16/deteksi-cabai"
HF_TOKEN = os.getenv("HF_TOKEN")
headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

async def predict_disease(image_bytes: bytes) -> dict:
    if not HF_TOKEN:
        raise HTTPException(status_code=500, detail="HF_TOKEN environment variable is not set")

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            HF_API_URL,
            headers=headers,
            files={"file": ("image.jpg", image_bytes, "image/jpeg")}
        )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"Hugging Face API error: {response.text}")

    return response.json()
