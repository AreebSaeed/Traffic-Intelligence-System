import joblib
import pandas as pd

model = joblib.load("ml/models/xgboost_model.pkl")


def predict(data):

    df = pd.DataFrame([data])

    # columns used while training
    df["road_id"] = 0

    df["temperature_x"] = df.pop("temperature")
    df["humidity_x"] = df.pop("humidity")
    df["rain_x"] = df.pop("rain")
    df["wind_speed_x"] = df.pop("wind_speed")
    df["cloud_cover_x"] = df.pop("cloud_cover")

    # API doesn't send these
    df["morning_peak"] = 0
    df["evening_peak"] = 0

    # EXACT training order
    df = df[
        [
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
    ]

    prediction = model.predict(df)[0]

    labels = {
        0: "Low Traffic",
        1: "Medium Traffic",
        2: "High Traffic"
    }

    return labels[prediction]