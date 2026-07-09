from pathlib import Path
import osmnx as ox

place = "Karachi, Sindh, Pakistan"

print("Downloading Karachi road network...")
graph = ox.graph_from_place(place, network_type="drive")

print("Converting to GeoDataFrames...")
nodes, edges = ox.graph_to_gdfs(graph)

output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "karachi_roads.geojson"

print(f"Saving to {output_file}...")
edges.to_file(output_file, driver="GeoJSON")

print("✅ Download completed successfully!")