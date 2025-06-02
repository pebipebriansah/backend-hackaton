from pydantic import BaseModel

class HargaRingkasResponse(BaseModel):
    harga_bulan_ini: float
    harga_bulan_lalu: float
    # Optional: tambahkan tren jika dibutuhkan
    # tren: str

    class Config:
        orm_mode = True
