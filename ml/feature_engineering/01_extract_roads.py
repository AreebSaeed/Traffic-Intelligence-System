import geopandas as gpd
import pandas as pd

from config import INTERMEDIATE_DIR, PROJECT_ROOT, ROADS_OUTPUT


def extract_roads() -> pd.DataFrame:
    roads_path = PROJECT_ROOT / "data" / "processed" / "roads_clean.geojson"
    if not roads_path.exists():
        roads_path = PROJECT_ROOT / "data" / "raw" / "karachi_roads.geojson"

    roads = gpd.read_file(roads_path)

    features = roads[
        ["osmid", "name", "highway", "length", "lanes", "maxspeed"]
    ].copy()

    features.rename(
        columns={
            "osmid": "road_osm_id",
            "name": "road_name",
            "highway": "road_type",
        },
        inplace=True,
    )

    features["road_name"] = features["road_name"].fillna("Unnamed Road")
    features["length"] = pd.to_numeric(features["length"], errors="coerce")
    features = features[features["length"] > 0]

    return features


if __name__ == "__main__":
    INTERMEDIATE_DIR.mkdir(parents=True, exist_ok=True)
    roads_df = extract_roads()
    roads_df.to_csv(ROADS_OUTPUT, index=False)
    print(f"Saved {len(roads_df)} road records to {ROADS_OUTPUT}")
