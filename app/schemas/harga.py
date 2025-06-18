from pydantic import BaseModel, HttpUrl, validator
from typing import List, Optional, Union

class HargaCabai(BaseModel):
    nama: str
    harga: int
    satuan: str
    tanggal: str
    gambar: Optional[Union[HttpUrl, str]] = None  # HttpUrl kadang error kalau file .jpg (non-URL aman)
    sumber: Optional[str] = None
    kondisi_harga: Optional[str] = None

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
    message: str
    success: int
    data: List[HargaCabai]

    class Config:
        schema_extra = {
            "example": {
                "message": "Get data successfull",
                "success": 1,
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
