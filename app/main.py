from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import router dari package app.routes
from app.routes import authPetani, petani

# Import database dari app.database (sesuai contoh sebelumnya)
from app.database import Base, engine

# Buat semua tabel jika belum ada
Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:5173",  # untuk development frontend (React/Vite)
    "https://frontend-hackaton-ggro.vercel.app",  # jika kamu nanti deploy frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # sesuaikan domain asal jika mau dibatasi
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authPetani.router, prefix="/auth", tags=["Auth"])
app.include_router(petani.router, prefix="/petani", tags=["Petani"])
