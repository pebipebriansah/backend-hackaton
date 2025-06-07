from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import authPetani, petani, rekomendasi, cuaca, harga, predict
from app.database import Base, engine

# Inisialisasi database
Base.metadata.create_all(bind=engine)

# Inisialisasi aplikasi FastAPI
app = FastAPI(
    title="Backend Petani",
    description="API untuk login, data petani, cuaca, rekomendasi, harga pertanian, dan deteksi penyakit cabai",
    version="1.0.0"
)

# Konfigurasi CORS agar bisa diakses dari frontend React (local & Azure)
origins = [
    "http://localhost:5173",  # Untuk development 
    "http://localhost:5000",
    "http://localhost:8081",
    "https://salmon-sky-06cf0f700.6.azurestaticapps.net",  # Untuk production di Azure Static Web Apps
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Daftarkan semua router
app.include_router(authPetani.router, prefix="/auth", tags=["Auth"])
app.include_router(petani.router, prefix="/petani", tags=["Petani"])
app.include_router(rekomendasi.router, prefix="/rekomendasi", tags=["Rekomendasi"])
app.include_router(cuaca.router, prefix="/cuaca", tags=["Cuaca"])
app.include_router(harga.router, prefix="/harga", tags=["Harga"])
app.include_router(predict.router, prefix="/deteksi", tags=["Deteksi"])
