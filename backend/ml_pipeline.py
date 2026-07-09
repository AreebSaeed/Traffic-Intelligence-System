"""Loads the trained model and builds feature vectors for live predictions."""

import re
from datetime import datetime
from pathlib import Path

import joblib
import pandas as pd
import requests

from database import engine


def parse_road_id(value) -> int:
    """Extract the first numeric id (some roads store merged ids as '[id1, id2]')."""
    match = re.search(r"\d+", str(value))
    return int(match.group()) if match else 0


def clean_text(value) -> str:
    """Turn stringified lists like "['Shahrah-e-Faisal']" into plain text."""
    text_value = str(value)
    parts = re.findall(r"'([^']*)'", text_value)
    if parts:
        return ", ".join(dict.fromkeys(parts))
    return text_value


def match_road_type(value: str) -> str:
    """Map a plain road type ('residential') to its stored key ("['residential']")."""
    needle = str(value).strip().lower()
    for key in ROAD_TYPE_MAPPING:
        if needle and needle in key.lower():
            return key
    return next(iter(ROAD_TYPE_MAPPING))

PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = PROJECT_ROOT / "ml" / "models" / "xgboost_model.pkl"
TARGET_ENCODER_PATH = PROJECT_ROOT / "ml" / "models" / "target_encoder.pkl"

# Exact columns (and order) the XGBoost model was trained on.
FEATURE_COLUMNS = [
    "road_id",
    "road_type",
    "length",
    "lanes",
    "maxspeed",
    "temperature_x",
    "humidity_x",
    "rain_x",
    "wind_speed_x",
    "cloud_cover_x",
    "hour",
    "day",
    "month",
    "weekday",
    "is_weekend",
    "morning_peak",
    "evening_peak",
    "is_holiday",
    "school_peak",
    "office_peak",
    "event",
]

KARACHI_LATITUDE = 24.8607
KARACHI_LONGITUDE = 67.0011

model = joblib.load(MODEL_PATH)
target_encoder = joblib.load(TARGET_ENCODER_PATH)

# road_type was label-encoded during training (sorted unique values).
# Rebuild the same mapping from the roads table.
_road_types = pd.read_sql("SELECT DISTINCT road_type FROM roads", engine)
ROAD_TYPE_MAPPING = {
    value: index
    for index, value in enumerate(sorted(_road_types["road_type"].astype(str)))
}


def get_current_weather() -> dict:
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={KARACHI_LATITUDE}"
        f"&longitude={KARACHI_LONGITUDE}"
        "&current=temperature_2m,relative_humidity_2m,rain,"
        "wind_speed_10m,cloud_cover"
        "&timezone=Asia/Karachi"
    )
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    current = response.json()["current"]
    return {
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "rain": current["rain"],
        "wind_speed": current["wind_speed_10m"],
        "cloud_cover": current["cloud_cover"],
    }


def get_context_flags(now: datetime) -> dict:
    """Holiday / school / office / event flags for the given moment."""
    today = now.date()
    hour = now.hour

    holidays = pd.read_sql("SELECT holiday_date FROM holidays", engine)
    holiday_dates = set(pd.to_datetime(holidays["holiday_date"]).dt.date)
    is_holiday = int(today in holiday_dates)

    schools = pd.read_sql(
        "SELECT opening_time, closing_time FROM school_timings", engine
    )
    school_peak = 0
    for _, row in schools.iterrows():
        open_hour = int(str(row["opening_time"]).split(":")[0])
        close_hour = int(str(row["closing_time"]).split(":")[0])
        if open_hour - 1 <= hour <= close_hour:
            school_peak = 1
            break

    offices = pd.read_sql(
        "SELECT opening_time, closing_time FROM office_timings", engine
    )
    office_peak = 0
    for _, row in offices.iterrows():
        open_hour = int(str(row["opening_time"]).split(":")[0])
        close_hour = int(str(row["closing_time"]).split(":")[0])
        if open_hour <= hour <= close_hour:
            office_peak = 1
            break

    events = pd.read_sql("SELECT event_date FROM events", engine)
    event_dates = set(pd.to_datetime(events["event_date"]).dt.date)
    event = int(today in event_dates)

    return {
        "is_holiday": is_holiday,
        "school_peak": school_peak,
        "office_peak": office_peak,
        "event": event,
    }


def build_features(
    roads: pd.DataFrame,
    weather: dict,
    context: dict,
    now: datetime,
) -> pd.DataFrame:
    """Build the model feature matrix for one or many roads."""
    features = pd.DataFrame()

    features["road_id"] = roads["road_id"].map(parse_road_id)
    features["road_type"] = (
        roads["road_type"].astype(str).map(ROAD_TYPE_MAPPING).fillna(0).astype(int)
    )
    features["length"] = pd.to_numeric(roads["length"], errors="coerce")
    features["lanes"] = pd.to_numeric(roads["lanes"], errors="coerce")
    features["maxspeed"] = pd.to_numeric(roads["maxspeed"], errors="coerce")

    features["temperature_x"] = weather["temperature"]
    features["humidity_x"] = weather["humidity"]
    features["rain_x"] = weather["rain"]
    features["wind_speed_x"] = weather["wind_speed"]
    features["cloud_cover_x"] = weather["cloud_cover"]

    features["hour"] = now.hour
    features["day"] = now.day
    features["month"] = now.month
    features["weekday"] = now.weekday()
    features["is_weekend"] = int(now.weekday() in (5, 6))
    features["morning_peak"] = int(7 <= now.hour <= 9)
    features["evening_peak"] = int(16 <= now.hour <= 19)

    features["is_holiday"] = context["is_holiday"]
    features["school_peak"] = context["school_peak"]
    features["office_peak"] = context["office_peak"]
    features["event"] = context["event"]

    features = features.fillna(0)
    return features[FEATURE_COLUMNS]


def predict(features: pd.DataFrame) -> tuple[list[str], list[float]]:
    """Return (labels, confidences) for a feature matrix."""
    probabilities = model.predict_proba(features)
    class_indices = probabilities.argmax(axis=1)
    labels = target_encoder.inverse_transform(class_indices)
    confidences = probabilities.max(axis=1)
    return labels.tolist(), confidences.round(4).tolist()
