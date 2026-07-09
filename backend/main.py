from datetime import datetime

import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import text

import ml_pipeline
from database import engine

app = FastAPI(title="Karachi Traffic Intelligence API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Bulk prediction interval in minutes (15, 30, or 60).
SCHEDULE_INTERVAL_MINUTES = 15


class PredictRequest(BaseModel):
    road_id: int


class ManualPredictRequest(BaseModel):
    road_type: str = "residential"
    length: float = 250
    lanes: float = 2
    maxspeed: float = 60
    temperature: float = 30
    humidity: float = 60
    rain: float = 0
    hour: int = 12


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def fetch_road(road_id: int) -> pd.Series:
    # road_id is stored as text; merged roads hold lists like "[id1, id2]",
    # so match the id as a whole word anywhere in the value.
    road = pd.read_sql(
        text(r"SELECT * FROM roads WHERE road_id ~ :pattern LIMIT 1"),
        engine,
        params={"pattern": rf"\y{road_id}\y"},
    )
    if road.empty:
        raise HTTPException(status_code=404, detail=f"Road {road_id} not found")
    return road.iloc[0]


def save_predictions(rows: list[dict]) -> None:
    frame = pd.DataFrame(rows)
    frame.to_sql(
        "predictions",
        engine,
        if_exists="append",
        index=False,
        chunksize=5000,
        method="multi",
    )


def run_prediction_for_roads(roads: pd.DataFrame) -> list[dict]:
    now = datetime.now()
    weather = ml_pipeline.get_current_weather()
    context = ml_pipeline.get_context_flags(now)

    features = ml_pipeline.build_features(roads, weather, context, now)
    labels, confidences = ml_pipeline.predict(features)

    return [
        {
            "road_id": int(features.iloc[i]["road_id"]),
            "road_name": ml_pipeline.clean_text(roads.iloc[i]["road_name"]),
            "prediction": labels[i],
            "confidence": confidences[i],
            "temperature": weather["temperature"],
            "humidity": weather["humidity"],
            "rain": weather["rain"],
            "datetime": now,
        }
        for i in range(len(roads))
    ]


# ------------------------------------------------------------------
# Step 4.2 – Roads API
# ------------------------------------------------------------------

@app.get("/roads")
def get_roads(limit: int = Query(default=1000, le=10000), offset: int = 0):
    roads = pd.read_sql(
        text(
            "SELECT road_id, road_name, road_type, "
            "ST_AsGeoJSON(geometry) AS geometry "
            "FROM roads ORDER BY road_id LIMIT :limit OFFSET :offset"
        ),
        engine,
        params={"limit": limit, "offset": offset},
    )
    return [
        {
            "road_id": ml_pipeline.parse_road_id(row["road_id"]),
            "name": ml_pipeline.clean_text(row["road_name"]),
            "geometry": row["geometry"],
            "road_type": ml_pipeline.clean_text(row["road_type"]),
        }
        for _, row in roads.iterrows()
    ]


# ------------------------------------------------------------------
# Step 4.3 – Road Search API
# ------------------------------------------------------------------

@app.get("/roads/search")
def search_roads(name: str, limit: int = Query(default=50, le=500)):
    roads = pd.read_sql(
        text(
            "SELECT road_id, road_name, "
            "ST_AsGeoJSON(geometry) AS geometry FROM roads "
            "WHERE road_name ILIKE :pattern ORDER BY road_name LIMIT :limit"
        ),
        engine,
        params={"pattern": f"%{name}%", "limit": limit},
    )
    return [
        {
            "road_id": ml_pipeline.parse_road_id(row["road_id"]),
            "name": ml_pipeline.clean_text(row["road_name"]),
            "geometry": row["geometry"],
        }
        for _, row in roads.iterrows()
    ]


# ------------------------------------------------------------------
# Step 4.5 – Current Weather API
# ------------------------------------------------------------------

@app.get("/weather/current")
def current_weather():
    weather = ml_pipeline.get_current_weather()
    return {
        "temperature": weather["temperature"],
        "humidity": weather["humidity"],
        "rain": weather["rain"],
        "wind_speed": weather["wind_speed"],
    }


# ------------------------------------------------------------------
# Step 4.4 / 4.6 – Predict by Road ID
# ------------------------------------------------------------------

@app.post("/predict")
def predict_road(request: PredictRequest):
    return _predict_single(request.road_id)


@app.get("/predict/{road_id}")
def predict_road_by_id(road_id: int):
    return _predict_single(road_id)


def _predict_single(road_id: int):
    road = fetch_road(road_id)
    rows = run_prediction_for_roads(road.to_frame().T)
    save_predictions(rows)

    result = rows[0]
    return {
        "road_name": result["road_name"],
        "prediction": f"{result['prediction']} Traffic",
        "confidence": result["confidence"],
        "updated_at": result["datetime"].isoformat(timespec="seconds"),
    }


# ------------------------------------------------------------------
# Manual prediction (custom feature input from the frontend form)
# ------------------------------------------------------------------

@app.post("/predict-manual")
def predict_manual(request: ManualPredictRequest):
    now = datetime.now().replace(hour=max(0, min(23, request.hour)), minute=0)

    weather = ml_pipeline.get_current_weather()
    weather["temperature"] = request.temperature
    weather["humidity"] = request.humidity
    weather["rain"] = request.rain

    context = ml_pipeline.get_context_flags(now)

    road = pd.DataFrame(
        [
            {
                "road_id": 0,
                "road_type": ml_pipeline.match_road_type(request.road_type),
                "length": request.length,
                "lanes": request.lanes,
                "maxspeed": request.maxspeed,
            }
        ]
    )

    features = ml_pipeline.build_features(road, weather, context, now)
    labels, confidences = ml_pipeline.predict(features)

    return {
        "prediction": labels[0],
        "label": f"{labels[0]} Traffic",
        "confidence": confidences[0],
        "updated_at": datetime.now().isoformat(timespec="seconds"),
    }


# ------------------------------------------------------------------
# Statistics for the dashboard
# ------------------------------------------------------------------

@app.get("/stats")
def stats():
    with engine.connect() as conn:
        total_roads = conn.execute(text("SELECT COUNT(*) FROM roads")).scalar()
        predictions_today = conn.execute(
            text("SELECT COUNT(*) FROM predictions WHERE datetime::date = CURRENT_DATE")
        ).scalar()
        average_speed = conn.execute(
            text(
                "SELECT AVG(substring(maxspeed FROM '\\d+')::float) "
                "FROM roads WHERE maxspeed IS NOT NULL"
            )
        ).scalar()
        distribution = conn.execute(
            text(
                "SELECT prediction, COUNT(*) FROM ("
                "SELECT prediction FROM predictions ORDER BY datetime DESC LIMIT 5000"
                ") recent GROUP BY prediction"
            )
        ).fetchall()

    return {
        "total_roads": int(total_roads or 0),
        "predictions_today": int(predictions_today or 0),
        "average_speed": round(float(average_speed or 0), 1),
        "traffic_distribution": {row[0]: row[1] for row in distribution},
    }


# ------------------------------------------------------------------
# Step 4.7 – Bulk Prediction
# ------------------------------------------------------------------

@app.post("/predict-all")
def predict_all(limit: int | None = None):
    query = "SELECT * FROM roads ORDER BY road_id"
    if limit:
        query += f" LIMIT {int(limit)}"

    roads = pd.read_sql(text(query), engine)
    rows = run_prediction_for_roads(roads)
    save_predictions(rows)

    return {
        "roads_predicted": len(rows),
        "saved_to": "predictions",
        "updated_at": datetime.now().isoformat(timespec="seconds"),
    }


# ------------------------------------------------------------------
# Prediction history
# ------------------------------------------------------------------

@app.get("/predictions/history")
def prediction_history(road_id: int | None = None, limit: int = Query(default=100, le=1000)):
    if road_id is not None:
        query = text(
            "SELECT * FROM predictions WHERE road_id = :road_id "
            "ORDER BY datetime DESC LIMIT :limit"
        )
        params = {"road_id": road_id, "limit": limit}
    else:
        query = text("SELECT * FROM predictions ORDER BY datetime DESC LIMIT :limit")
        params = {"limit": limit}

    history = pd.read_sql(query, engine, params=params)
    history["datetime"] = history["datetime"].astype(str)
    return history.to_dict(orient="records")


# ------------------------------------------------------------------
# Step 4.8 – Scheduled Predictions
# ------------------------------------------------------------------

def scheduled_bulk_prediction():
    print(f"[scheduler] Running bulk prediction at {datetime.now()}")
    try:
        roads = pd.read_sql("SELECT * FROM roads ORDER BY road_id", engine)
        rows = run_prediction_for_roads(roads)
        save_predictions(rows)
        print(f"[scheduler] Saved {len(rows)} predictions.")
    except Exception as exc:
        print(f"[scheduler] Bulk prediction failed: {exc}")


scheduler = BackgroundScheduler()
scheduler.add_job(
    scheduled_bulk_prediction,
    "interval",
    minutes=SCHEDULE_INTERVAL_MINUTES,
    max_instances=1,
    coalesce=True,
)


@app.on_event("startup")
def start_scheduler():
    scheduler.start()


@app.on_event("shutdown")
def stop_scheduler():
    scheduler.shutdown(wait=False)
