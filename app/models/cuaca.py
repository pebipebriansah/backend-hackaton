from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from app.database import Base
class Cuaca(Base):
    __tablename__ = "cuaca"

    id_cuaca = Column(Integer, primary_key=True, index=True)
    id_petani = Column(Integer, ForeignKey("tbl_petani.id_petani"), nullable=False)
    lokasi = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    curah_hujan = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
