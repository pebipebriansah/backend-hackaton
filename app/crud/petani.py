from sqlalchemy.orm import Session
from app.models.petani import Petani
from app.utils.security import hash_password

def get_petani_by_email(db: Session, email: str):
    return db.query(Petani).filter(Petani.email == email).first()

def create_petani(db: Session, petani_data):
    hashed_pw = hash_password(petani_data.password)
    db_petani = Petani(
        nama_petani=petani_data.nama_petani,
        alamat=petani_data.alamat,
        email=petani_data.email,
        telepon=petani_data.telepon,
        password=hashed_pw
    )
    db.add(db_petani)
    db.commit()
    db.refresh(db_petani)
    return db_petani