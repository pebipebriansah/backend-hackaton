import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx

router = APIRouter(prefix="/rekomendasi", tags=["Rekomendasi"])

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

class KeluhanInput(BaseModel):
    keluhan: str

class RekomendasiOutput(BaseModel):
    rekomendasi: str

@router.post("/", response_model=RekomendasiOutput)
async def get_rekomendasi(data: KeluhanInput):
    prompt = f"Berikan rekomendasi cara mengatasi masalah berikut pada tanaman: {data.keluhan}. Jawab dengan singkat dan jelas."

    headers = {
        "api-key": AZURE_OPENAI_KEY,
        "Content-Type": "application/json",
    }
    body = {
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200,
        "temperature": 0.7,
    }

    url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2023-05-15"

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=body)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Gagal mengambil rekomendasi dari Azure OpenAI")

        result = response.json()
        rekomendasi = result["choices"][0]["message"]["content"].strip()

    return {"rekomendasi": rekomendasi}
