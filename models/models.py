from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
    Text,
)
from models.base_model import RequiredField
from geoalchemy2 import Geometry


class PolygonData(RequiredField):
    __tablename__ = "polygons"

    id = Column(Integer, primary_key=True, index=True)
    geom = Column(Geometry("POLYGON", srid=4326), nullable=False)
    properties = Column(JSON, nullable=True)


# class LineData(RequiredField):
#     __tablename__ = "lines"

#     id = Column(Integer, primary_key=True, index=True)
#     geom = Column(Geometry(geometry_type="LINESTRING", srid=4326), nullable=False)
#     name = Column(String(50), nullable=True)


# class PointData(RequiredField):
#     __tablename__ = "points"

#     id = Column(Integer, primary_key=True, index=True)
#     geom = Column(Geometry(geometry_type="POINT", srid=4326), nullable=False)
#     name = Column(String(50), nullable=True)
