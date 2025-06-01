from fastapi import APIRouter
from app.schemas.rekomendasi import RekomendasiRequest, RekomendasiResponse
from app.crud.rekomendasi import generate_rekomendasi_openai

router = APIRouter()

@router.post("/", response_model=RekomendasiResponse)
def buat_rekomendasi(req: RekomendasiRequest):
    hasil = generate_rekomendasi_openai(req.keluhan)
    return {"rekomendasi": hasil}
