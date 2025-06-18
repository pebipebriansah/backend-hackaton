from fastapi import APIRouter, HTTPException
from app.schemas.harga import HargaCabaiResponse, HargaCabai
from app.scrapper.scrapper import ambil_harga_cabai
from pydantic import ValidationError

router = APIRouter()

@router.get("/", response_model=HargaCabaiResponse, summary="Ambil data harga cabai terbaru")
def get_harga_cabai():
    # Ambil data dari scrapper
    try:
        data_scraped = ambil_harga_cabai()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal mengambil data: {e}")
    
    if not data_scraped:
        raise HTTPException(status_code=404, detail="Data harga cabai tidak ditemukan.")

    # Debug log data mentah
    print("✅ DATA MENTAH:", data_scraped)

    try:
        harga_cabai_list = [HargaCabai(**item) for item in data_scraped]
    except ValidationError as e:
        print("❌ VALIDATION ERROR:", e)
        raise HTTPException(status_code=422, detail="Validasi data harga cabai gagal.")

    # Debug log data hasil parsing
    print("✅ DATA TERVALIDASI:", harga_cabai_list)

    return HargaCabaiResponse(data=harga_cabai_list)
