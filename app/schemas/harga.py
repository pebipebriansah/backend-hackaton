from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class HargaCabai(BaseModel):
    nama: str
    harga: int
    satuan: str
    tanggal: str
    gambar: Optional[HttpUrl] = None  # validasi URL otomatis
    sumber: Optional[str] = None      # nama instansi, misalnya "Dinas Perindustrian dan Perdagangan"
    kondisi_harga: Optional[str] = None  # naik / turun / tetap

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "nama": "Cabai Hijau Biasa",
                "harga": 25000,
                "satuan": "kg",
                "tanggal": "2025-06-15",
                "gambar": "https://data.jabarprov.go.id/api-dashboard-jabar/static/upload/abc.svg",
                "sumber": "Dinas Perindustrian dan Perdagangan",
                "kondisi_harga": "tetap"
            }
        }

class HargaCabaiResponse(BaseModel):
    data: List[HargaCabai]

    class Config:
        schema_extra = {
            "example": {
                "data": [
                    {
                        "nama": "Cabai Hijau Biasa",
                        "harga": 25000,
                        "satuan": "kg",
                        "tanggal": "2025-06-15",
                        "gambar": "https://data.jabarprov.go.id/api-dashboard-jabar/static/upload/abc.svg",
                        "sumber": "Dinas Perindustrian dan Perdagangan",
                        "kondisi_harga": "tetap"
                    }
                ]
            }
        }
