from pydantic import BaseModel
from typing import Optional


class HargaRingkasResponse(BaseModel):
    harga_bulan_ini: float
    harga_bulan_lalu: float
    class Config:
        orm_mode = True
class HargaPrediksiResponse(BaseModel):
    harga_bulan_ini: float
    harga_bulan_lalu: float
    harga_bulan_depan: float
    confidence: Optional[float] = None  # contoh persentase keyakinan prediksi
