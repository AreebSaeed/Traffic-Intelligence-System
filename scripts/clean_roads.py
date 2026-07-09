import geopandas as gpd
import pandas as pd
from pathlib import Path

print("Loading roads...")
roads = gpd.read_file("data/raw/karachi_roads.geojson")

# Keep only useful columns
roads = roads[
    [
        "osmid",
        "name",
        "highway",
        "length",
        "lanes",
        "maxspeed",
        "geometry",
    ]
]

# Rename columns
roads.rename(
    columns={
        "osmid": "road_id",
        "name": "road_name",
        "highway": "road_type",
    },
    inplace=True,
)

# Replace missing names
roads["road_name"] = roads["road_name"].fillna("Unnamed Road")

# Convert length
roads["length"] = pd.to_numeric(roads["length"], errors="coerce")

# Remove roads with invalid length
roads = roads[roads["length"] > 0]

# # Remove duplicates
# import json

# for col in ["road_id", "road_name", "road_type"]:
#     roads[col] = roads[col].apply(
#         lambda x: json.dumps(x) if isinstance(x, list) else x
#     )
# roads = roads.drop_duplicates()
# Create processed folder
Path("data/processed").mkdir(parents=True, exist_ok=True)

# Save
roads.to_file(
    "data/processed/roads_clean.geojson",
    driver="GeoJSON"
)

print("\nCleaning Complete!")
print(f"Total Roads: {len(roads)}")
print(roads.head())