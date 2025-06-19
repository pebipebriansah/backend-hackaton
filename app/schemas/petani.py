from pydantic import BaseModel,EmailStr
from typing import Optional
class PetaniLogin(BaseModel):
    email: str
    password: str
class TokenData(BaseModel):
    access_token: str
    token_type: str
class TokenWithInfo(TokenData):
    email: EmailStr
    nama_petani: str
    id_petani : int
    telepon: str
    alamat: str
    foto_profil: str | None = None
    
class PetaniRegister(BaseModel):
    nama_petani: str
    alamat: str
    email: EmailStr
    telepon: str
    password: str
    foto_profil: str | None = None
class PetaniResponse(BaseModel):
    id_petani: int
    nama_petani: str
    alamat: str
    email: EmailStr
    telepon: str
    foto_profil: str | None = None
class PetaniUpdate(BaseModel):
    nama_petani: Optional[str] = None  
    alamat: Optional[str] = None
    email: Optional[EmailStr] = None
    telepon: Optional[str] = None
    foto_profil: Optional[str] = None
    
    class Config:
        from_attributes = True
