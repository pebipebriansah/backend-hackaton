from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import harga as crud
from app.schemas.harga import HargaRingkasResponse  # sesuaikan nama

router = APIRouter(prefix="/harga", tags=["Harga"])

@router.get("/", response_model=HargaRingkasResponse)
def read_harga_bulan_ini_lalu(db: Session = Depends(get_db)):
    return crud.get_harga_bulan_ini_dan_lalu(db)
