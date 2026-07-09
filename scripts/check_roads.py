import geopandas as gpd

roads = gpd.read_file("data/raw/karachi_roads.geojson")

print(roads.head())
print()

print("Number of roads:", len(roads))
print()

print(roads.columns)
print()

print(roads["highway"].value_counts().head(20))