from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.petani import PetaniRegister, PetaniResponse
from app.crud.petani import create_petani
from app.database import get_db
from app.models.petani import Petani

router = APIRouter()

@router.post("/register", response_model=PetaniResponse)
def register_petani(petani: PetaniRegister, db: Session = Depends(get_db)):
    # Cek email sudah dipakai atau belum
    existing = db.query(Petani).filter(Petani.email == petani.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email sudah digunakan"
        )
    new_petani = create_petani(db, petani)
    return new_petani