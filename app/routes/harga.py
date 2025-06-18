from fastapi import APIRouter, HTTPException
from app.schemas.harga import HargaCabaiResponse, HargaCabai
from app.scrapper.scrapper import ambil_harga_cabai
from pydantic import ValidationError

router = APIRouter()

@router.get("/", response_model=HargaCabaiResponse)
def get_harga_cabai():
    data_scraped = ambil_harga_cabai()
    if not data_scraped:
        raise HTTPException(status_code=500, detail="Gagal mengambil data harga cabai.")
    
    try:
        # Validasi dan konversi ke dict sesuai skema Pydantic
        harga_cabai_list = [HargaCabai(**item).dict() for item in data_scraped]
    except ValidationError as e:
        # Tambahkan log di sini jika perlu
        raise HTTPException(status_code=500, detail="Validasi data harga cabai gagal.")

    return {"data": harga_cabai_list}
