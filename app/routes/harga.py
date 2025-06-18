from fastapi import APIRouter, HTTPException
from app.schemas.harga import HargaCabaiResponse, HargaCabai
from app.scrapper.scrapper import ambil_harga_cabai

router = APIRouter()

@router.get("/", response_model=HargaCabaiResponse)
def get_harga_cabai():
    data_scraped = ambil_harga_cabai()
    if not data_scraped:
        raise HTTPException(status_code=500, detail="Gagal mengambil data harga cabai.")
    
    harga_cabai_list = [HargaCabai(**item) for item in data_scraped]
    return {"data": harga_cabai_list}
