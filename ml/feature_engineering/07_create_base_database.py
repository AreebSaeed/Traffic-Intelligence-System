import pandas as pd
from config import engine

print("=" * 60)
print("Creating Base Dataset...")
print("=" * 60)

# Load roads from Supabase
roads = pd.read_sql("SELECT * FROM roads", engine)

# Load weather from Supabase
weather = pd.read_sql("SELECT * FROM weather", engine)
weather["datetime"] = pd.to_datetime(weather["datetime"])

print(f"Roads: {len(roads):,}")
print(f"Weather Records: {len(weather):,}")

# -------------------------------------------------------------------
# IMPORTANT
# -------------------------------------------------------------------
# We DO NOT create 500,268 × 168 rows (84 million rows).
# For the portfolio project we sample roads.
# Increase SAMPLE_SIZE later if you want.
# -------------------------------------------------------------------

SAMPLE_SIZE = 5000

roads = roads.sample(
    n=min(SAMPLE_SIZE, len(roads)),
    random_state=42
).reset_index(drop=True)

print(f"Using {len(roads):,} sampled roads")

rows = []

for _, road in roads.iterrows():

    for _, w in weather.iterrows():

        rows.append({

            "road_id": road["road_id"],

            "road_name": road["road_name"],

            "road_type": road["road_type"],

            "length": road["length"],

            "lanes": road["lanes"],

            "maxspeed": road["maxspeed"],

            "geometry": road["geometry"],

            "prediction_datetime": w["datetime"],

            "temperature": w["temperature"],

            "humidity": w["humidity"],

            "rain": w["rain"],

            "wind_speed": w["wind_speed"],

            "cloud_cover": w["cloud_cover"]

        })

base = pd.DataFrame(rows)

print("\nBase Dataset Created")

print(base.head())

print()

print("Shape:")

print(base.shape)

base.to_csv(

    "ml/datasets/base_dataset.csv",

    index=False

)

print()

print("Saved Successfully!")

print("File: ml/datasets/base_dataset.csv")