from fastapi import APIRouter, Depends
from app.schemas.rekomendasi import KeluhanInput, RekomendasiOutput
from app.crud.rekomendasi import generate_rekomendasi
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status
from jose import JWTError, jwt
from app.config import SECRET_KEY, ALGORITHM

router = APIRouter(
    prefix="/rekomendasi",
    tags=["Rekomendasi"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/", response_model=RekomendasiOutput)
def get_rekomendasi(data: KeluhanInput, email: str = Depends(verify_token)):
    hasil = generate_rekomendasi(data.keluhan)
    return {"rekomendasi": hasil}
