from sqlalchemy.orm import Session
from app.models.cuaca import Cuaca
from app.schemas.cuaca import CuacaCreate
from datetime import datetime, timedelta

def simpan_cuaca(db: Session, data: CuacaCreate):
    rekomendasi = None
    sekarang = datetime.utcnow()
    tujuh_hari_lalu = sekarang - timedelta(days=6)

    # Ambil data curah hujan 6 hari terakhir + hari ini (7 hari total)
    data_hujan = db.query(Cuaca).filter(
        Cuaca.id_petani == data.id_petani,
        Cuaca.lokasi == data.lokasi,
        Cuaca.created_at >= tujuh_hari_lalu,
        Cuaca.curah_hujan > 0
    ).order_by(Cuaca.created_at.desc()).limit(6).all()

    # Jika sudah hujan 6 hari terakhir dan hari ini juga hujan
    if len(data_hujan) == 6 and data.curah_hujan > 0:
        rekomendasi = "Berikan vitamin tanaman karena hujan selama 7 hari berturut-turut"

    cuaca_baru = Cuaca(
        id_petani=data.id_petani,
        lokasi=data.lokasi,
        latitude=data.latitude,
        longitude=data.longitude,
        curah_hujan=data.curah_hujan,
        rekomendasi=rekomendasi,
        created_at=sekarang
    )
    db.add(cuaca_baru)
    db.commit()
    db.refresh(cuaca_baru)
    return cuaca_baru