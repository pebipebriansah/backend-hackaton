from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import harga as crud
from app.schemas.harga import HargaRingkasResponse  # sesuaikan nama

router = APIRouter(prefix="/harga", tags=["Harga"])

@router.get("/", response_model=HargaRingkasResponse)
def read_harga_bulan_ini_lalu(db: Session = Depends(get_db)):
    return crud.get_harga_bulan_ini_dan_lalu(db)
@router.get("/prediksi")
def read_prediksi_harga(db: Session = Depends(get_db)):
    harga_prediksi, mse = crud.predict_harga_bulan_depan(db)
    if harga_prediksi is None:
        return {"error": "Data tidak cukup untuk prediksi"}
    return {
        "harga_bulan_depan": harga_prediksi,
        "mean_squared_error": mse
    }
