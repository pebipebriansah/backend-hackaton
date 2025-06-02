from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import get_db
from app.schemas.cuaca import CuacaCreate, CuacaOut
from app.models.cuaca import Cuaca  # model ORM tabel cuaca

router = APIRouter(
    prefix="/cuaca",
    tags=["Cuaca"]
)

HUJAN_THRESHOLD = 0.1  # Minimal curah hujan dianggap hujan

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

    tanggal_7_hari_lalu = datetime.utcnow() - timedelta(days=7)
    data_cuaca_7_hari = (
        db.query(Cuaca)
        .filter(
            Cuaca.id_petani == data.id_petani,
            Cuaca.latitude == data.latitude,
            Cuaca.longitude == data.longitude,
            Cuaca.created_at >= tanggal_7_hari_lalu
        )
        .order_by(Cuaca.created_at.asc())
        .all()
    )

    if len(data_cuaca_7_hari) < 7:
        rekomendasi = "Data cuaca kurang dari 7 hari, tunggu data lebih lengkap."
    else:
        hari_hujan_beruntun = 0
        max_hari_beruntun = 0
        for cuaca in data_cuaca_7_hari:
            if cuaca.curah_hujan > HUJAN_THRESHOLD:
                hari_hujan_beruntun += 1
                max_hari_beruntun = max(max_hari_beruntun, hari_hujan_beruntun)
            else:
                hari_hujan_beruntun = 0

        if max_hari_beruntun >= 7:
            rekomendasi = (
                "Curah hujan terjadi selama lebih dari 7 hari berturut-turut. "
                "Disarankan memberikan vitamin pada tanaman cabai."
            )
        else:
            rekomendasi = "Curah hujan normal, lanjutkan perawatan tanaman seperti biasa."

    return CuacaOut(
        id_cuaca=db_cuaca.id_cuaca,
        id_petani=db_cuaca.id_petani,
        lokasi=db_cuaca.lokasi,
        latitude=db_cuaca.latitude,
        longitude=db_cuaca.longitude,
        curah_hujan=db_cuaca.curah_hujan,
        created_at=db_cuaca.created_at,
        rekomendasi=rekomendasi
    )

