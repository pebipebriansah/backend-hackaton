from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CuacaCreate(BaseModel):
    id_petani: int
    lokasi: str
    latitude: float
    longitude: float
    curah_hujan: float
    created_at: Optional[datetime] = None  # Jika tidak dikirim, bisa di-set otomatis di DB

class CuacaOut(BaseModel):
    id_cuaca: int
    id_petani: int
    lokasi: str
    latitude: float
    longitude: float
    curah_hujan: float
    rekomendasi: Optional[str] = None
    created_at: datetime
class CuacaRekomendasiResponse(BaseModel):
    rekomendasi: str
    class Config:
        from_attributes = True


