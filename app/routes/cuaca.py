from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.schemas.cuaca import CuacaCreate, CuacaOut
from app.models.cuaca import Cuaca  # model ORM tabel cuaca

router = APIRouter(
    prefix="/cuaca",
    tags=["Cuaca"]
)

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
