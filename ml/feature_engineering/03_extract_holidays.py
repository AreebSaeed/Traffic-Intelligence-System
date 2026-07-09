import pandas as pd
from sqlalchemy import create_engine

from config import DATABASE_URL, HOLIDAYS_OUTPUT, INTERMEDIATE_DIR, PROJECT_ROOT


def extract_holidays() -> pd.DataFrame:
    engine = create_engine(DATABASE_URL)

    try:
        holidays = pd.read_sql("SELECT * FROM holidays", engine)
    except Exception:
        holidays = pd.read_csv(PROJECT_ROOT / "data" / "external" / "holidays.csv")

    holidays["holiday_date"] = pd.to_datetime(holidays["holiday_date"])
    return holidays


if __name__ == "__main__":
    INTERMEDIATE_DIR.mkdir(parents=True, exist_ok=True)
    holidays_df = extract_holidays()
    holidays_df.to_csv(HOLIDAYS_OUTPUT, index=False)
    print(f"Saved {len(holidays_df)} holiday records to {HOLIDAYS_OUTPUT}")
