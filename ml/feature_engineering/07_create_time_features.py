import pandas as pd

from config import INTERMEDIATE_DIR, TIME_OUTPUT, WEATHER_OUTPUT


def create_time_features(weather_path=WEATHER_OUTPUT) -> pd.DataFrame:
    weather = pd.read_csv(weather_path, parse_dates=["datetime"])

    time_features = weather[["datetime"]].copy()
    time_features["date"] = time_features["datetime"].dt.date
    time_features["hour"] = time_features["datetime"].dt.hour
    time_features["day_of_week"] = time_features["datetime"].dt.dayofweek
    time_features["day_name"] = time_features["datetime"].dt.day_name()
    time_features["month"] = time_features["datetime"].dt.month
    time_features["is_weekend"] = time_features["day_of_week"].isin([5, 6]).astype(int)
    time_features["is_rush_hour"] = time_features["hour"].isin([8, 9, 17, 18, 19]).astype(int)

    return time_features


if __name__ == "__main__":
    INTERMEDIATE_DIR.mkdir(parents=True, exist_ok=True)
    time_df = create_time_features()
    time_df.to_csv(TIME_OUTPUT, index=False)
    print(f"Saved {len(time_df)} time feature records to {TIME_OUTPUT}")
