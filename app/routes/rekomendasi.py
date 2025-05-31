from fastapi import APIRouter
from app.schemas.rekomendasi import KeluhanInput, RekomendasiOutput
from app.crud.rekomendasi import generate_rekomendasi

router = APIRouter(prefix="/rekomendasi", tags=["Rekomendasi"])

@router.post("/", response_model=RekomendasiOutput)
def get_rekomendasi(data: KeluhanInput):
    hasil = generate_rekomendasi(data.keluhan)
    return {"rekomendasi": hasil}
