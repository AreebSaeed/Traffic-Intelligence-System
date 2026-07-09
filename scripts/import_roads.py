import json

import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = (
    "postgresql://postgres.qxgoagigfcnhawsuthvs:ktis_proj_1234"
    "@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
)


def normalize_id(value):
    if isinstance(value, list):
        return value[0] if value else None
    return value


def normalize_text(value):
    if value is None:
        return None
    if isinstance(value, list):
        return json.dumps(value)
    if hasattr(value, "tolist"):
        return json.dumps(value.tolist())
    return str(value) if not isinstance(value, str) else value


print("Connecting to Supabase...")
engine = create_engine(DATABASE_URL)

print("Reading GeoJSON...")
roads = gpd.read_file("data/raw/karachi_roads.geojson")

# Keep only required columns
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

roads.rename(
    columns={
        "osmid": "road_osm_id",
        "name": "road_name",
        "highway": "road_type",
    },
    inplace=True,
)

roads["road_name"] = roads["road_name"].fillna("Unnamed Road")
roads["road_osm_id"] = roads["road_osm_id"].apply(normalize_id)
roads["lanes"] = roads["lanes"].apply(normalize_text)
roads["maxspeed"] = roads["maxspeed"].apply(normalize_text)
roads["length"] = pd.to_numeric(roads["length"], errors="coerce")

print(f"Uploading {len(roads)} roads...")

roads.to_postgis(
    "roads",
    engine,
    if_exists="replace",   # use "append" after the first import
    index=False
)

print("Upload complete!")