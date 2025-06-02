from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CuacaCreate(BaseModel):
    id_petani: int
    lokasi: str
    latitude: float
    longitude: float
    curah_hujan: float
    created_at: Optional[datetime] = None  # tidak wajib diisi

class CuacaOut(CuacaCreate):
    id_cuaca: int
    rekomendasi: str | None = None
    created_at: datetime

    class Config:
        orm_mode = True
