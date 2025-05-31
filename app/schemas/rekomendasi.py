from pydantic import BaseModel

class KeluhanInput(BaseModel):
    keluhan: str

class RekomendasiOutput(BaseModel):
    rekomendasi: str
