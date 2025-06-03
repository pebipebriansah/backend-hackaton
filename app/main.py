from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import router dari package app.routes
from app.routes import authPetani, petani, rekomendasi, cuaca, harga, predict  # ✅ Tambahkan predict

# Import database dari app.database
from app.database import Base, engine

# Buat semua tabel jika belum ada
Base.metadata.create_all(bind=engine)

# Inisialisasi aplikasi FastAPI
app = FastAPI(
    title="Backend Petani",
    description="API untuk login, data petani, cuaca, rekomendasi, dan harga pertanian",
    version="1.0.0"
)

# Domain frontend yang diperbolehkan mengakses backend
origins = [
    "http://localhost:5173",  # untuk development lokal
    "https://salmon-sky-06cf0f700.6.azurestaticapps.net",  # frontend deploy
]

# Konfigurasi CORS
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
app.include_router(harga.router, prefix="/harga", tags=["Harga"])  # ✅ Tambahkan router harga
app.include_router(predict.router, prefix="/deteksi", tags=["Deteksi"])  # ✅ Perbaikan di sini
