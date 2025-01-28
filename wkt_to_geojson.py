"""
Convet WKT To geojson
"""

import geopandas as gpd
from shapely.wkt import loads

# Define the WKT polygon
wkt_polygon = "POLYGON((-90 66.5482634621744,-90 66.51326044311185,-89.912109375 66.51326044311185,-89.912109375 66.5482634621744,-90 66.5482634621744))"

# Convert the WKT polygon to a Shapely geometry
geometry = loads(wkt_polygon)

# Create a GeoDataFrame
gdf = gpd.GeoDataFrame([{"geometry": geometry}], crs="EPSG:4326")

gdf.to_file("test.geojson", driver="GeoJSON")
