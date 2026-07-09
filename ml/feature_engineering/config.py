from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_URL = (
    "postgresql://postgres.qxgoagigfcnhawsuthvs:ktis_proj_1234"
    "@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
)

DATASETS_DIR = PROJECT_ROOT / "ml" / "datasets"
INTERMEDIATE_DIR = DATASETS_DIR / "intermediate"
FINAL_DATASET_PATH = DATASETS_DIR / "traffic_dataset.csv"

KARACHI_LATITUDE = 24.8607
KARACHI_LONGITUDE = 67.0011
TIMEZONE = "Asia/Karachi"

ROADS_OUTPUT = INTERMEDIATE_DIR / "roads_features.csv"
WEATHER_OUTPUT = INTERMEDIATE_DIR / "weather_features.csv"
HOLIDAYS_OUTPUT = INTERMEDIATE_DIR / "holidays_features.csv"
SCHOOL_OUTPUT = INTERMEDIATE_DIR / "school_features.csv"
OFFICE_OUTPUT = INTERMEDIATE_DIR / "office_features.csv"
EVENTS_OUTPUT = INTERMEDIATE_DIR / "events_features.csv"
TIME_OUTPUT = INTERMEDIATE_DIR / "time_features.csv"
MERGED_OUTPUT = INTERMEDIATE_DIR / "merged_features.csv"
LABELED_OUTPUT = INTERMEDIATE_DIR / "labeled_features.csv"
