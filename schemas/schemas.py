from pydantic import BaseModel, Field
from typing import Any, Dict, List, Union


class PolygonCreate(BaseModel):
    geojson: Any = Field(..., description="GeoJSON of the polygon")


class PolygonRead(PolygonCreate):
    id: int
    properties: Dict[str, Any]  # Storing properties as a dictionary

    class Config:
        orm_mode = True
