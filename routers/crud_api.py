from fastapi import FastAPI, Depends, HTTPException, APIRouter, status
from sqlalchemy.exc import NoResultFound
from postgis.database import get_db
from utils.crud import create_polygon, get_polygon, update_polygon, delete_polygon
from schemas.schemas import PolygonCreate, PolygonRead
from sqlalchemy.orm import Session
from typing import Annotated
from geoalchemy2.functions import ST_AsGeoJSON
import json
from utils.config.logger import logger

router = APIRouter(prefix="/api", tags=["api"])
db_dependency = Annotated[Session, Depends(get_db)]


# Here in PolygonRead schemas dict format only return
@router.post("/polygons/", response_model=PolygonRead)
async def create_polygon_api(polygon: PolygonCreate, db: db_dependency):
    try:
        created_polygon = create_polygon(db, polygon)
        logger.info(
            f"created_polygon info: {created_polygon}, {created_polygon.id}, {created_polygon.geom}"
        )

        # return {
        #     "status": status.HTTP_201_CREATED,
        #     "message": "Polygon created successfully",
        #     "data": polygon,
        # }

        return {
            "id": created_polygon.id,
            "geojson": {
                "type": "Feature",
                "geometry": json.loads(
                    db.scalar(ST_AsGeoJSON(created_polygon.geom))
                ),  # Ensure this is converted correctly
                "properties": created_polygon.properties,
            },
        }
    except Exception as e:
        logger.error(f"An unexpected error occurred while creating polygon. Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating polygon. Error {}".format(
                e
            ),
        )


@router.get("/polygons/{polygon_id}/", response_model=PolygonRead)
async def read_polygon_api(polygon_id: int, db: db_dependency):
    try:
        return get_polygon(db, polygon_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Polygon not found")


@router.put("/polygons/{polygon_id}/")
async def update_polygon_api(
    polygon_id: int, polygon: PolygonCreate, db: db_dependency
):
    try:
        updated_polygon = update_polygon(db, polygon_id, polygon)
        logger.info(
            f"updated_polygon info: {updated_polygon}, {updated_polygon.id}, {updated_polygon.geom}"
        )

        return {
            "status": status.HTTP_201_CREATED,
            "message": "Polygon updated successfully",
            "data": polygon,
        }

        # return {
        #     "id": updated_polygon.id,
        #     "geojson": {
        #         "type": "Feature",
        #         "geometry": json.loads(
        #             db.scalar(ST_AsGeoJSON(updated_polygon.geom))
        #         ),  # Ensure this is converted correctly
        #         "properties": updated_polygon.properties,
        #     },
        # }
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Polygon not found"
        )


@router.delete("/polygons/{polygon_id}/")
async def delete_polygon_api(polygon_id: int, db: db_dependency):
    try:
        delete_polygon(db, polygon_id)

        return {
            "status": status.HTTP_200_OK,
            "message": "Polygon deleted successfully.",
        }
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Polygon not found"
        )
