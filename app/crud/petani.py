from sqlalchemy.orm import Session
from app.models.petani import Petani
from app.utils.security import hash_password

def get_petani_by_email(db: Session, email: str):
    return db.query(Petani).filter(Petani.email == email).first()

def update_petani(db: Session, petani_id: int, petani_data):
    db_petani = db.query(Petani).filter(Petani.id_petani == petani_id).first()
    if not db_petani:
        return None
    if hasattr(petani_data, 'nama_petani'):
        db_petani.nama_petani = petani_data.nama_petani
    if hasattr(petani_data, 'alamat'):
        db_petani.alamat = petani_data.alamat
    if hasattr(petani_data, 'email'):
        db_petani.email = petani_data.email
    if hasattr(petani_data, 'telepon'):
        db_petani.telepon = petani_data.telepon
    if hasattr(petani_data, 'password'):
        db_petani.password = hash_password(petani_data.password)
    if hasattr(petani_data, 'foto_profil'):
        db_petani.foto_profil = petani_data.foto_profil

    db.commit()
    db.refresh(db_petani)
    return db_petani
def create_petani(db: Session, petani_data):
    hashed_pw = hash_password(petani_data.password)
    db_petani = Petani(
        nama_petani=petani_data.nama_petani,
        alamat=petani_data.alamat,
        email=petani_data.email,
        telepon=petani_data.telepon,
        password=hashed_pw,
        foto_profil=petani_data.foto_profil if hasattr(petani_data, 'foto_profil') else None
    )
    db.add(db_petani)
    db.commit()
    db.refresh(db_petani)
    return db_petani