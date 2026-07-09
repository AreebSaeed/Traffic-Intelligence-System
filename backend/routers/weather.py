from fastapi import APIRouter

router = APIRouter()

@router.get("/weather")

def weather():

    return {

        "temperature": 32,

        "humidity": 68,

        "rain": 0,

        "wind_speed": 11

    }