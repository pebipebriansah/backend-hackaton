from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.database import Base

class Harga(Base):
    __tablename__ = "tabel_harga"

    id_harga = Column(Integer, primary_key=True, index=True)
    bulan = Column(String, nullable=False)
    tahun = Column(Integer, nullable=False)
    curah_hujan = Column(Float, nullable=False)
    harga = Column(Float, nullable=False)
    sumber = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
