import requests
import geopandas as gpd
import matplotlib.pyplot as plt

# Headers for OpenStreetMap request
headers = {
    "User-Agent": "<name> <email>",
    "Accept": "application/geo+json, application/json"
}

# Get data from endpoint
raw_data = requests.get(r'https://nominatim.openstreetmap.org/search?q=Roseburg,Oregon&format=geojson&polygon_geojson=1', headers=headers)

# Convert response to GeoJSON
json_data = raw_data.json()

# GeoJSON to GeoDataFrame
gdf = gpd.GeoDataFrame.from_features(json_data["features"], crs="EPSG:4326")

# Create map from GeoDataFrame and write to HTML file
export_map = gdf.explore("name", cmap=["Purple"], popup=["type", "place_rank"], tiles="CartoDB.Voyager", legend=True, tooltip=["display_name", "category", "type"])
out_file = "map.html"
export_map.save(out_file)