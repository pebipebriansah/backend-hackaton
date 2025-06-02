from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Cuaca(Base):
    __tablename__ = "cuaca"

    id = Column(Integer, primary_key=True, index=True)
    id_petani = Column(Integer, ForeignKey("tbl_petani.id_petani"), nullable=False)
    lokasi = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    curah_hujan = Column(Float, nullable=False)
    rekomendasi = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
