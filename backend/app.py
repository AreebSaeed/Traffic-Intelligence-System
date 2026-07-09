from fastapi import FastAPI

from backend.routers.prediction import router as prediction_router

from backend.routers.weather import router as weather_router

from backend.routers.roads import router as roads_router

app = FastAPI(

    title="Karachi Traffic Intelligence API",

    version="1.0.0"

)

app.include_router(prediction_router)

app.include_router(weather_router)

app.include_router(roads_router)


@app.get("/")

def home():

    return {

        "project": "Karachi Traffic Intelligence System",

        "status": "Running"

    }