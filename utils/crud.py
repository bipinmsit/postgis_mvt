from fastapi import APIRouter, status, Depends, HTTPException, Response
from geoalchemy2.shape import to_shape, from_shape
from shapely.geometry import shape
from models.models import PolygonData
from schemas.schemas import PolygonCreate
from sqlalchemy.orm import Session
from shapely.geometry import Polygon
from utils.config.logger import logger
from sqlalchemy.exc import SQLAlchemyError
from geoalchemy2.functions import ST_AsGeoJSON
import json


def create_polygon(db: Session, polygon_data: PolygonCreate):
    try:
        geojson = polygon_data.geojson
        polygon = Polygon(geojson["geometry"]["coordinates"][0])

        db_polygon = PolygonData(
            geom=from_shape(polygon, srid=4326), properties=geojson["properties"]
        )
        db.add(db_polygon)
        db.commit()
        db.refresh(db_polygon)

        return db_polygon
    except Exception as e:
        logger.error(f"Something went wrong in create_polygon method: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Something went wrong in create_polygon method: {e}",
        )


def get_polygon(db: Session, polygon_id: int):
    try:
        polygon = db.query(PolygonData).filter(PolygonData.id == polygon_id).first()
        if not polygon:
            return None

        return {
            "id": polygon.id,
            "geojson": {
                "type": "Feature",
                "geometry": json.loads(
                    db.scalar(ST_AsGeoJSON(polygon.geom))
                ),  # Convert to GeoJSON
                "properties": polygon.properties,
            },
            "properties": polygon.properties,
        }
    except Exception as e:
        logger.error(f"Something went wrong in get_polygon method: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Something went wrong in get_polygon method: {e}",
        )


def update_polygon(db: Session, polygon_id: int, polygon: PolygonCreate):
    try:
        db_polygon = db.query(PolygonData).filter(PolygonData.id == polygon_id).first()
        if not db_polygon:
            raise HTTPException(status_code=404, detail="Polygon not found.")

        # Extract only the 'geometry' part from GeoJSON
        geometry_data = polygon.geojson.get("geometry")

        if not geometry_data:
            raise HTTPException(
                status_code=400, detail="Invalid GeoJSON: Missing 'geometry' field."
            )

        # Extract and update geometry
        geometry_data = polygon.geojson.get("geometry")
        if not geometry_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid GeoJSON: Missing 'geometry' field.",
            )

        polygon_shape = shape(geometry_data)  # Convert geometry to Shapely shape
        db_polygon.geom = from_shape(
            polygon_shape, srid=4326
        )  # Assign SRID (EPSG:4326)

        # Extract and update properties
        properties_data = polygon.geojson.get("properties")
        if not properties_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid GeoJSON: Missing 'properties' field.",
            )

        db_polygon.properties = properties_data  # Update properties

        db.commit()
        db.refresh(db_polygon)

        return db_polygon

    except HTTPException:
        raise  # Re-raise FastAPI HTTP errors

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error while update Polygon: {str(e)}",
        )


def delete_polygon(db: Session, polygon_id: int):
    try:
        db_polygon = db.query(PolygonData).filter(PolygonData.id == polygon_id).first()

        if not db_polygon:
            raise HTTPException(status_code=404, detail="Polygon not found.")

        db.delete(db_polygon)
        db.commit()

    except SQLAlchemyError as db_err:
        db.rollback()  # Rollback the transaction on failure
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while deleting polygon",
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error while deleting polygon: {str(e)}",
        )
