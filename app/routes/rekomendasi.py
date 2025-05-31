from fastapi import FastAPI
from app.schemas.rekomendasi import RekomendasiRequest, RekomendasiResponse
from app.crud.rekomendasi import generate_rekomendasi_openai

app = FastAPI()

@app.post("/rekomendasi", response_model=RekomendasiResponse)
def buat_rekomendasi(req: RekomendasiRequest):
    hasil = generate_rekomendasi_openai(req.keluhan)
    return {"rekomendasi": hasil}
