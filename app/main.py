from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import authPetani, petani, rekomendasi, cuaca, harga, predict
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Backend Petani",
    description="API untuk login, data petani, cuaca, rekomendasi, dan harga pertanian",
    version="1.0.0"
)

origins = [
    "http://localhost:5173",
    "https://salmon-sky-06cf0f700.6.azurestaticapps.net",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authPetani.router, prefix="/auth", tags=["Auth"])
app.include_router(petani.router, prefix="/petani", tags=["Petani"])
app.include_router(rekomendasi.router, prefix="/rekomendasi", tags=["Rekomendasi"])
app.include_router(cuaca.router, prefix="/cuaca", tags=["Cuaca"])
app.include_router(harga.router, prefix="/harga", tags=["Harga"])
app.include_router(predict.router, prefix="/deteksi", tags=["Deteksi"])
