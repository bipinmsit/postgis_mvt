from fastapi import APIRouter, status, Depends, HTTPException, Response
import psycopg2
from utils.config.env import DB_CONFIG

# create router
router = APIRouter(prefix="/mvt", tags=["mvt"])

@router.get("/{layer_name}/{z}/{x}/{y}")
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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tile not found")

        # Return the tile with the correct MIME type
        return Response(
            content=mvt_tile, media_type="application/vnd.mapbox-vector-tile"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")