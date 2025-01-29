"""
Convet WKT To geojson
"""

import geopandas as gpd
from shapely.wkt import loads
import os


def wkt_to_geojson(wkt: str, output_geojson: str):
    """_summary_

    Args:
        wkt (str): WKT String
        output_geojson (str): Output GeoJSON
    Returns:
    """

    # Convert the WKT polygon to a Shapely geometry
    geometry = loads(wkt)

    # Create a GeoDataFrame
    gdf = gpd.GeoDataFrame([{"geometry": geometry}], crs="EPSG:4326")

    gdf.to_file(output_geojson, driver="GeoJSON")


# Define the WKT polygon
wkt_polygon = "POLYGON((-90 66.5482634621744,-90 66.51326044311185,-89.912109375 66.51326044311185,-89.912109375 66.5482634621744,-90 66.5482634621744))"
wkt_to_geojson(
    wkt_polygon, os.path.join(os.getcwd(), "utils\data\converted_json.geojson")
)
