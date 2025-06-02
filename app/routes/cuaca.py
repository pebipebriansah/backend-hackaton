from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.cuaca import CuacaCreate, CuacaOut
from app.crud import cuaca as crud_cuaca

router = APIRouter(
    prefix="/cuaca",
    tags=["Cuaca"]
)

@router.post("/", response_model=CuacaOut)
def create_cuaca(data: CuacaCreate, db: Session = Depends(get_db)):
    return crud_cuaca.simpan_cuaca(db, data)
