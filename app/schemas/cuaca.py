from pydantic import BaseModel
from datetime import datetime

class CuacaCreate(BaseModel):
    id_petani: int
    lokasi: str
    latitude: float
    longitude: float
    curah_hujan: float

class CuacaOut(CuacaCreate):
    id: int
    rekomendasi: str | None = None
    created_at: datetime

    class Config:
        orm_mode = True
