from pydantic import BaseModel

class HargaRingkasResponse(BaseModel):
    harga_bulan_ini: float
    harga_bulan_lalu: float
    class Config:
        orm_mode = True
