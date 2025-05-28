from sqlalchemy import Column, Integer, String
from app.database import Base

class Petani(Base):
    __tablename__ = "tbl_petani"

    id_petani = Column(Integer, primary_key=True, index=True)
    nama_petani = Column(String)
    alamat = Column(String)
    email = Column(String, unique=True, index=True)
    telepon = Column(String)
    password = Column(String)
