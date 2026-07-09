import pandas as pd
from sqlalchemy import create_engine

from config import DATABASE_URL, EVENTS_OUTPUT, INTERMEDIATE_DIR, PROJECT_ROOT


def extract_events() -> pd.DataFrame:
    engine = create_engine(DATABASE_URL)

    try:
        events = pd.read_sql("SELECT * FROM events", engine)
    except Exception:
        events = pd.read_csv(PROJECT_ROOT / "data" / "external" / "events.csv")

    events["event_date"] = pd.to_datetime(events["event_date"])
    return events


if __name__ == "__main__":
    INTERMEDIATE_DIR.mkdir(parents=True, exist_ok=True)
    events_df = extract_events()
    events_df.to_csv(EVENTS_OUTPUT, index=False)
    print(f"Saved {len(events_df)} event records to {EVENTS_OUTPUT}")
