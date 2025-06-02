from pydantic import BaseModel
from datetime import datetime

class CuacaCreate(BaseModel):
    id_petani: int
    lokasi: str
    latitude: float
    longitude: float
    curah_hujan: float
    create_at: datetime

class CuacaOut(CuacaCreate):
    id_cuaca: int
    rekomendasi: str | None = None
    created_at: datetime

    class Config:
        orm_mode = True
