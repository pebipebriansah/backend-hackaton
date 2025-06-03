from fastapi import APIRouter, UploadFile, File
from app.detector.detector import predict_disease

router = APIRouter()

@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = await predict_disease(image_bytes)
    return {"result": result}
