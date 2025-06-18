from pydantic import BaseModel
from typing import List

class HargaCabai(BaseModel):
    nama: str
    harga_bulan_ini: int
    harga_bulan_lalu: int
    satuan: str
    tanggal: str

class HargaCabaiResponse(BaseModel):
    data: List[HargaCabai]
