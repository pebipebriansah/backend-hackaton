from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.schemas.rekomendasi import KeluhanInput, RekomendasiOutput
from app.crud.rekomendasi import generate_rekomendasi
from app.config import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/rekomendasi", tags=["Rekomendasi"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # pastikan sesuai dengan prefix login

def verify_token(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token tidak valid: email tidak ditemukan",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return email
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/", response_model=RekomendasiOutput)
def get_rekomendasi(data: KeluhanInput, email: str = Depends(verify_token)):
    # email adalah user yg sedang login, bisa digunakan jika perlu
    hasil = generate_rekomendasi(data.keluhan)
    return {"rekomendasi": hasil}
