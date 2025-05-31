from pydantic import BaseModel

class RekomendasiRequest(BaseModel):
    keluhan: str

class RekomendasiResponse(BaseModel):
    rekomendasi: str
