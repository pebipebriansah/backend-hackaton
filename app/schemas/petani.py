from pydantic import BaseModel,EmailStr

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
    nama_petani: str | None = None
    alamat: str | None = None
    email: EmailStr | None = None
    telepon: str | None = None
    foto_profil: str | None = None
    
    class Config:
        from_attributes = True
