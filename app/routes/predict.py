from fastapi import APIRouter, UploadFile, File, HTTPException
from app.detector.detector import predict_disease
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Validasi: hanya file gambar yang diizinkan
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File yang diunggah harus berupa gambar.")

    try:
        # Baca isi file sebagai byte
        image_bytes = await file.read()

        # Jalankan deteksi
        result = await predict_disease(image_bytes)

        return {
            "success": True,
            "message": "Prediksi berhasil",
            "data": result  # ✅ Tidak nested
        }

    except HTTPException as http_error:
        # Error spesifik dari fungsi predict_disease (misalnya prediction gagal)
        logger.error(f"HTTPException saat prediksi: {http_error.detail}")
        raise http_error

    except Exception as e:
        # Error umum
        logger.exception("Unexpected error saat prediksi")
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan saat memproses gambar: {str(e)}")
