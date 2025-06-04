from fastapi import APIRouter, UploadFile, File, HTTPException
from app.detector.detector import predict_disease

router = APIRouter()

@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Validasi jenis file
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File harus berupa gambar")

    try:
        # Baca isi file sebagai bytes
        image_bytes = await file.read()

        # Panggil fungsi deteksi
        result = await predict_disease(image_bytes)

        return {
            "success": True,
            "message": "Prediksi berhasil",
            "data": result
        }

    except HTTPException as http_error:
        raise http_error

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan saat memproses gambar: {str(e)}")
