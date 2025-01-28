"""
Read this article carefully to get the context how ST_AsMVT Works

https://chatgpt.com/share/6798ac90-08bc-8008-bf2b-96be256cd311
"""

from fastapi import FastAPI, Response, HTTPException
import psycopg2

app = FastAPI()


# Database configuration
DB_CONFIG = {
    "dbname": "gis_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432,
}


@app.get("/mvt/{layer_name}/{z}/{x}/{y}")
def get_mvt_tile(layer_name: str, z: int, x: int, y: int):
    try:
        # Connect to the database
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Call the SQL function
        cursor.execute(
            "SELECT get_mvt_tile(%s, %s, %s, %s);",
            (layer_name, z, x, y),
        )
        mvt_tile = cursor.fetchone()[0]

        # Close the connection
        cursor.close()
        conn.close()

        if not mvt_tile:
            raise HTTPException(status_code=404, detail="Tile not found")

        # Return the tile with the correct MIME type
        return Response(
            content=mvt_tile, media_type="application/vnd.mapbox-vector-tile"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
