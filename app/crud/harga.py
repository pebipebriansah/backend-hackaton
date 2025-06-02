from sqlalchemy.orm import Session
from datetime import datetime

from app.models.harga import Harga

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

    harga_bulan_ini = (
        db.query(Harga)
        .filter(Harga.bulan == bulan_ini, Harga.tahun == tahun_ini)
        .first()
    )

    harga_bulan_lalu = (
        db.query(Harga)
        .filter(Harga.bulan == bulan_lalu, Harga.tahun == tahun_lalu)
        .first()
    )

    return {
        "harga_bulan_ini": harga_bulan_ini.harga if harga_bulan_ini else 0,
        "harga_bulan_lalu": harga_bulan_lalu.harga if harga_bulan_lalu else 0,
    }
