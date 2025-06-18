from fastapi import APIRouter
from app.schemas.harga import HargaCabaiResponse, HargaCabai
from app.scrapper import ambil_harga_cabai
router = APIRouter()
@router.get("/", response_model=HargaCabaiResponse)
def get_harga_cabai():
    # Mengambil data dari scraper
    data_scraped = ambil_harga_cabai()
    
    # Mengonversi data ke dalam format HargaCabai
    harga_cabai_list = [HargaCabai(**item) for item in data_scraped]
    
    return {"data": harga_cabai_list}