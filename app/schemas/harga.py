from pydantic import BaseModel
from typing import List

class HargaCabai(BaseModel):
    nama: str
    harga: int
    satuan: str
    kategori: str
    tanggal: str

class HargaCabaiResponse(BaseModel):
    data: List[HargaCabai]
    