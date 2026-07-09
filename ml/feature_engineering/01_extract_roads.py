import pandas as pd
from config import engine

print("=" * 60)
print("Extracting Road Data from Supabase...")
print("=" * 60)

query = """
SELECT
    road_osm_id,
    road_name,
    road_type,
    length,
    lanes,
    maxspeed,
    geometry
FROM roads;
"""

roads = pd.read_sql(query, engine)

print("\nRoads loaded successfully.\n")

print("Dataset Shape:")
print(roads.shape)

print("\nFirst Five Rows:")
print(roads.head())

print("\nColumn Names:")
print(list(roads.columns))

print("\nMissing Values:")
print(roads.isnull().sum())

print("\nRoad Types:")
print(roads["road_type"].value_counts().head(20))

print("\nAverage Road Length:")
print(round(roads["length"].mean(), 2), "meters")

print("\nLongest Road:")
print(round(roads["length"].max(), 2), "meters")

print("\nSaving extracted dataset...")

roads.to_csv(
    "ml/datasets/roads_raw.csv",
    index=False
)

print("\nRoad dataset saved successfully!")

print("\nSaved to:")
print("ml/datasets/roads_raw.csv")