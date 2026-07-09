import pandas as pd
from sqlalchemy import create_engine

from config import DATABASE_URL, INTERMEDIATE_DIR, OFFICE_OUTPUT, PROJECT_ROOT


def extract_office() -> pd.DataFrame:
    engine = create_engine(DATABASE_URL)

    try:
        office = pd.read_sql("SELECT * FROM office_timings", engine)
    except Exception:
        office = pd.read_csv(PROJECT_ROOT / "data" / "external" / "office_timings.csv")

    office["opening_time"] = pd.to_datetime(office["opening_time"], format="%H:%M:%S").dt.time
    office["closing_time"] = pd.to_datetime(office["closing_time"], format="%H:%M:%S").dt.time
    return office


if __name__ == "__main__":
    INTERMEDIATE_DIR.mkdir(parents=True, exist_ok=True)
    office_df = extract_office()
    office_df.to_csv(OFFICE_OUTPUT, index=False)
    print(f"Saved {len(office_df)} office timing records to {OFFICE_OUTPUT}")
