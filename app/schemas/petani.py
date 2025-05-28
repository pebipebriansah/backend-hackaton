from pydantic import BaseModel,EmailStr

class PetaniLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class PetaniRegister(BaseModel):
    nama_petani: str
    alamat: str
    email: EmailStr
    telepon: str
    password: str
    
class PetaniResponse(BaseModel):
    id_petani: int
    nama_petani: str
    alamat: str
    email: EmailStr
    telepon: str

    class Config:
        orm_mode = True
