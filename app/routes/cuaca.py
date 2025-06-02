from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.cuaca import CuacaCreate, CuacaOut
from crud import cuaca as crud_cuaca

router = APIRouter(
    prefix="/cuaca",
    tags=["Cuaca"]
)

@router.post("/", response_model=CuacaOut)
def create_cuaca(data: CuacaCreate, db: Session = Depends(get_db)):
    return crud_cuaca.simpan_cuaca(db, data)
