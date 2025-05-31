from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import router dari package app.routes
from app.routes import authPetani, petani, rekomendasi  # Tambahkan rekomendasi

# Import database dari app.database
from app.database import Base, engine

# Buat semua tabel jika belum ada
Base.metadata.create_all(bind=engine)

# Inisialisasi aplikasi FastAPI
app = FastAPI(
    title="Backend Petani",
    description="API untuk login, data petani, dan rekomendasi pertanian",
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
