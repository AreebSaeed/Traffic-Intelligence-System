import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine

DATABASE_URL = (
    "postgresql://postgres.qxgoagigfcnhawsuthvs:ktis_proj_1234"
    "@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
)

engine = create_engine(DATABASE_URL)

datasets = [
    {
        "table": "weather",
        "path": "ml/datasets/weather_raw.csv",
        "type": "csv"
    },
    {
        "table": "holidays",
        "path": "data/external/holidays.csv",
        "type": "csv"
    },
    {
        "table": "schools",
        "path": "data/external/school_timings.csv",
        "type": "csv"
    },
    {
        "table": "offices",
        "path": "data/external/office_timings.csv",
        "type": "csv"
    },
    {
        "table": "events",
        "path": "data/external/events.csv",
        "type": "csv"
    },
    {
        "table": "traffic_dataset",
        "path": "ml/datasets/final_dataset_encoded.csv",
        "type": "csv"
    }
]

print("=" * 60)
print("Uploading CSV datasets")
print("=" * 60)

for d in datasets:

    print(f"\nUploading {d['table']}...")

    df = pd.read_csv(d["path"])

    df.to_sql(
        d["table"],
        engine,
        if_exists="replace",
        index=False,
        chunksize=5000,
        method="multi"
    )

    print(f"✓ {len(df)} rows uploaded.")

print("\nUploading roads...")

roads = gpd.read_file("data/processed/roads_clean.geojson")

roads.to_postgis(
    "roads",
    engine,
    if_exists="replace",
    index=False
)

print(f"✓ {len(roads)} roads uploaded.")

print("\n")
print("=" * 60)
print("ALL DATA IMPORTED SUCCESSFULLY")
print("=" * 60)