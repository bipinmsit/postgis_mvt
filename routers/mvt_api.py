from fastapi import APIRouter, status, Depends, HTTPException, Response
import psycopg2
from utils.config.env import DB_CONFIG

# create router
router = APIRouter(prefix="/mvt", tags=["mvt"])


@router.get("/{layer_name}/{z}/{x}/{y}")
def get_mvt_tile(layer_name: str, z: int, x: int, y: int):
    try:

        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT get_mvt_tile(%s, %s, %s, %s);",
            (layer_name, z, x, y),
        )
        result = cursor.fetchone()

        if not result or len(result[0]) < 100:  # Minimum tile size check
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        return Response(
            content=(
                result[0].tobytes()
                if isinstance(result[0], memoryview)
                else bytes(result[0])
            ),
            media_type="application/vnd.mapbox-vector-tile",
        )

    except Exception as e:
        print(f"Tile error: {str(e)}")
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        if "conn" in locals():
            conn.close()
