from sqlalchemy.orm import Session
from sqlalchemy import extract
from app.models.harga import Harga
from datetime import datetime, timedelta

def get_harga_bulan_ini_dan_lalu(db: Session):
    today = datetime.today()
    bulan_ini = today.month
    tahun_ini = today.year

    # Hitung bulan lalu
    if bulan_ini == 1:
        bulan_lalu = 12
        tahun_lalu = tahun_ini - 1
    else:
        bulan_lalu = bulan_ini - 1
        tahun_lalu = tahun_ini

    # Ambil harga berdasarkan bulan sekarang dan bulan kemarin
    return db.query(Harga).filter(
        (extract('month', Harga.tanggal) == bulan_ini) & (extract('year', Harga.tanggal) == tahun_ini) |
        (extract('month', Harga.tanggal) == bulan_lalu) & (extract('year', Harga.tanggal) == tahun_lalu)
    ).all()
