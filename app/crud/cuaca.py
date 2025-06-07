from sqlalchemy.orm import Session
from app.models.cuaca import Cuaca
from app.schemas.cuaca import CuacaCreate
from datetime import datetime

def simpan_cuaca(db: Session, data: CuacaCreate):
    sekarang = datetime.utcnow()

    cuaca_baru = Cuaca(
        id_petani=data.id_petani,
        lokasi=data.lokasi,
        latitude=data.latitude,
        longitude=data.longitude,
        curah_hujan=data.curah_hujan,
        rekomendasi=None,  # Kosongkan atau hilangkan jika tidak diperlukan di model
        created_at=sekarang
    )

    db.add(cuaca_baru)
    db.commit()
    db.refresh(cuaca_baru)
    return cuaca_baru
