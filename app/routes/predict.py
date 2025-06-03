from fastapi import APIRouter, UploadFile, File, HTTPException
from app.detector.detector import predict_disease

router = APIRouter()

@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Validasi tipe file, hanya image yang diterima
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File harus berupa gambar")

    # Baca file sebagai bytes
    image_bytes = await file.read()

    try:
        result = await predict_disease(image_bytes)
    except HTTPException as e:
        # Forward HTTPException dari predict_disease
        raise e
    except Exception as e:
        # Tangani error lain
        raise HTTPException(status_code=500, detail=str(e))

    return {"result": result}
