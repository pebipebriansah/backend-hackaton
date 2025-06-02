from sqlalchemy.orm import Session
from sqlalchemy import extract
from app.models.harga import Harga
from datetime import datetime

def get_harga_bulan_ini_dan_lalu(db: Session):
    today = datetime.today()
    bulan_ini = today.month
    tahun_ini = today.year

    if bulan_ini == 1:
        bulan_lalu = 12
        tahun_lalu = tahun_ini - 1
    else:
        bulan_lalu = bulan_ini - 1
        tahun_lalu = tahun_ini

    return db.query(Harga).filter(
        (
            (extract('month', Harga.created_at) == bulan_ini) &
            (extract('year', Harga.created_at) == tahun_ini)
        ) | (
            (extract('month', Harga.created_at) == bulan_lalu) &
            (extract('year', Harga.created_at) == tahun_lalu)
        )
    ).all()
