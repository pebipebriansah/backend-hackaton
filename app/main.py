from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import rekomendasi, predict

# Inisialisasi aplikasi FastAPI
app = FastAPI(
    title="Backend Petani",
    description="API untuk login, data petani, cuaca, rekomendasi, harga pertanian, dan deteksi penyakit cabai",
    version="1.0.0"
)

# Konfigurasi CORS agar bisa diakses dari frontend React (local & Azure)
origins = [
    "http://localhost:5173",  # Untuk production di Azure Static Web Apps
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(rekomendasi.router, prefix="/rekomendasi", tags=["Rekomendasi"])
app.include_router(predict.router, prefix="/deteksi", tags=["Deteksi"])
