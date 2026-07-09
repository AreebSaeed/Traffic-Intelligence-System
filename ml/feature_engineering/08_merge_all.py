import pandas as pd

from config import (
    EVENTS_OUTPUT,
    HOLIDAYS_OUTPUT,
    INTERMEDIATE_DIR,
    MERGED_OUTPUT,
    TIME_OUTPUT,
    WEATHER_OUTPUT,
)


def merge_all() -> pd.DataFrame:
    time_df = pd.read_csv(TIME_OUTPUT, parse_dates=["datetime"])
    weather_df = pd.read_csv(WEATHER_OUTPUT, parse_dates=["datetime"])
    holidays_df = pd.read_csv(HOLIDAYS_OUTPUT, parse_dates=["holiday_date"])
    events_df = pd.read_csv(EVENTS_OUTPUT, parse_dates=["event_date"])

    merged = time_df.merge(weather_df, on="datetime", how="left")
    merged["date"] = pd.to_datetime(merged["date"])

    holiday_dates = set(holidays_df["holiday_date"].dt.date)
    event_dates = set(events_df["event_date"].dt.date)

    merged["is_holiday"] = merged["date"].dt.date.isin(holiday_dates).astype(int)
    merged["is_event_day"] = merged["date"].dt.date.isin(event_dates).astype(int)
    merged["event_count"] = merged["date"].dt.date.map(
        events_df.groupby(events_df["event_date"].dt.date).size()
    ).fillna(0).astype(int)

    return merged


if __name__ == "__main__":
    INTERMEDIATE_DIR.mkdir(parents=True, exist_ok=True)
    merged_df = merge_all()
    merged_df.to_csv(MERGED_OUTPUT, index=False)
    print(f"Saved {len(merged_df)} merged records to {MERGED_OUTPUT}")
