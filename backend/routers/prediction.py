from fastapi import APIRouter

from backend.models import PredictionRequest

from backend.predictor import predict

router = APIRouter()

@router.post("/predict")

def make_prediction(request: PredictionRequest):

    result = predict(request.dict())

    return result