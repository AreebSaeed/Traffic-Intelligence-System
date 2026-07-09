import pandas as pd
from sqlalchemy import create_engine

from config import DATABASE_URL, INTERMEDIATE_DIR, WEATHER_OUTPUT


def extract_weather() -> pd.DataFrame:
    engine = create_engine(DATABASE_URL)
    weather = pd.read_sql("SELECT * FROM weather ORDER BY datetime", engine)
    weather["datetime"] = pd.to_datetime(weather["datetime"])
    return weather


if __name__ == "__main__":
    INTERMEDIATE_DIR.mkdir(parents=True, exist_ok=True)
    weather_df = extract_weather()
    weather_df.to_csv(WEATHER_OUTPUT, index=False)
    print(f"Saved {len(weather_df)} weather records to {WEATHER_OUTPUT}")
