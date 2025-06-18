from fastapi import APIRouter
from app.schemas import HargaCabai, HargaCabaiResponse
from app.scrapper import ambil_harga_cabai

router = APIRouter()

@router.get("/", response_model=HargaCabaiResponse)
def get_harga_cabai():
    data_scraped = ambil_harga_cabai()
    return {"data": data_scraped}
