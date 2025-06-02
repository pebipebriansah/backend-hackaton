from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.crud import harga as crud
from app.schemas.harga import HargaResponse

router = APIRouter(prefix="/harga", tags=["Harga"])

@router.get("/", response_model=List[HargaResponse])
def read_harga_bulan_ini_lalu(db: Session = Depends(get_db)):
    return crud.get_harga_bulan_ini_dan_lalu(db)
