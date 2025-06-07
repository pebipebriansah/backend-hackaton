from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.schemas.cuaca import CuacaCreate, CuacaRekomendasiResponse, CuacaOut
from app.models.cuaca import Cuaca  # model ORM tabel cuaca

router = APIRouter()

@router.post("/", response_model=CuacaOut)
def create_cuaca(data: CuacaCreate, db: Session = Depends(get_db)):
    db_cuaca = Cuaca(
        id_petani=data.id_petani,
        lokasi=data.lokasi,
        latitude=data.latitude,
        longitude=data.longitude,
        curah_hujan=data.curah_hujan,
        created_at=data.created_at or datetime.utcnow()
    )
    db.add(db_cuaca)
    db.commit()
    db.refresh(db_cuaca)

    return CuacaOut(
        id_cuaca=db_cuaca.id_cuaca,
        id_petani=db_cuaca.id_petani,
        lokasi=db_cuaca.lokasi,
        latitude=db_cuaca.latitude,
        longitude=db_cuaca.longitude,
        curah_hujan=db_cuaca.curah_hujan,
        created_at=db_cuaca.created_at
    )
@router.get("/rekomendasi/{id_petani}", response_model=CuacaRekomendasiResponse)
def get_rekomendasi_cuaca_by_petani(id_petani: int, db: Session = Depends(get_db)):
    data_cuaca = (
        db.query(Cuaca)
        .filter(Cuaca.id_petani == id_petani)
        .order_by(Cuaca.created_at.desc())
        .limit(7)
        .all()
    )

    if len(data_cuaca) < 7:
        rekomendasi = "Data cuaca kurang dari 7 hari, tunggu data lebih lengkap."
    elif all(c.curah_hujan > 0.1 for c in data_cuaca):
        rekomendasi = "Berikan vitamin karena hujan 7 hari berturut-turut."
    else:
        rekomendasi = "Cuaca normal, lanjutkan perawatan biasa."

    return {"rekomendasi": rekomendasi}

