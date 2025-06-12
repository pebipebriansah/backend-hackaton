from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from app.database import get_db, SessionLocal
from app.schemas.petani import PetaniRegister, PetaniLogin, PetaniResponse, TokenWithInfo, PetaniUpdate
from app.models.petani import Petani
from app.crud.petani import create_petani, get_petani_by_email
from app.crud.petani import update_petani as update_petani_crud
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="petani/login")

# Password utils
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Token creator
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Get Current Petani
def get_current_petani(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Petani:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    petani = db.query(Petani).filter(Petani.email == email).first()
    if petani is None:
        raise credentials_exception
    return petani
    
# ========== REGISTER ==========
@router.post("/register", response_model=PetaniResponse)
def register_petani(petani: PetaniRegister, db: Session = Depends(get_db)):
    existing = db.query(Petani).filter(Petani.email == petani.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email sudah digunakan"
        )
    new_petani = create_petani(db, petani)
    return new_petani
# ========== LOGIN ==========
@router.post("/login", response_model=TokenWithInfo)
def login(petani: PetaniLogin, db: Session = Depends(get_db)):
    db_petani = get_petani_by_email(db, petani.email)
    if not db_petani or not verify_password(petani.password, db_petani.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token(
        data={"sub": db_petani.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "id_petani": db_petani.id_petani,
        "email": db_petani.email,
        "nama_petani": db_petani.nama_petani,
        "foto_profil": db_petani.foto_profil,
        "alamat": db_petani.alamat,
        "telepon": db_petani.telepon,
    }
# ========== UPDATE DATA PETANI ==========
@router.put("/update/{id_petani}", response_model=PetaniResponse)
def update_petani(id_petani: int, petani_data: PetaniUpdate, db: Session = Depends(get_db)):
    db_petani = db.query(Petani).filter(Petani.id_petani == id_petani).first()
    updated_petani = update_petani_crud(db, id_petani, petani_data)
    if not db_petani:
        raise HTTPException(status_code=404, detail="Petani not found")
    return updated_petani
    
# ========== VERIFIKASI TOKEN ==========
@router.get("/me", response_model=PetaniResponse)
def read_petani_me(current_petani: Petani = Depends(get_current_petani)):
    return current_petani
