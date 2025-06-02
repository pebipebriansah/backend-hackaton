from pydantic import BaseModel
from datetime import datetime

class HargaResponse(BaseModel):
    id_harga: int
    bulan: int  # jika di DB bulan disimpan sebagai integer
    tahun: int
    curah_hujan: float
    harga: float
    sumber: str
    created_at: datetime

    class Config:
        orm_mode = True
