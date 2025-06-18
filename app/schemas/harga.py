from pydantic import BaseModel
from typing import List, Optional

class HargaCabai(BaseModel):
    nama: str
    harga: int
    satuan: str
    tanggal: str
    gambar: Optional[str] = None  # jika ingin sertakan URL gambar dari API

class HargaCabaiResponse(BaseModel):
    data: List[HargaCabai]
