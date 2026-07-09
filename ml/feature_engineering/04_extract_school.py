import pandas as pd
from sqlalchemy import create_engine

from config import DATABASE_URL, INTERMEDIATE_DIR, PROJECT_ROOT, SCHOOL_OUTPUT


def extract_school() -> pd.DataFrame:
    engine = create_engine(DATABASE_URL)

    try:
        school = pd.read_sql("SELECT * FROM school_timings", engine)
    except Exception:
        school = pd.read_csv(PROJECT_ROOT / "data" / "external" / "school_timings.csv")

    school["opening_time"] = pd.to_datetime(school["opening_time"], format="%H:%M:%S").dt.time
    school["closing_time"] = pd.to_datetime(school["closing_time"], format="%H:%M:%S").dt.time
    return school


if __name__ == "__main__":
    INTERMEDIATE_DIR.mkdir(parents=True, exist_ok=True)
    school_df = extract_school()
    school_df.to_csv(SCHOOL_OUTPUT, index=False)
    print(f"Saved {len(school_df)} school timing records to {SCHOOL_OUTPUT}")
