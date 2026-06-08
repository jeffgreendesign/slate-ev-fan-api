import json
from pathlib import Path
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.vehicle import Vehicle, Feature
from app.schemas.vehicle import Vehicle as VehicleSchema
from app.schemas.vehicle import Feature as FeatureSchema

router = APIRouter()


def _load_sources() -> dict[str, Any]:
    sources_path = Path("data/slate_sources.json")
    if not sources_path.exists():
        raise HTTPException(status_code=404, detail="Source metadata not found")
    return json.loads(sources_path.read_text(encoding="utf-8"))

@router.get("/", response_model=VehicleSchema)
async def get_vehicle(db: Session = Depends(get_db)):
    """Get the main vehicle information."""
    vehicle = db.query(Vehicle).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

@router.get("/features", response_model=List[FeatureSchema])
async def get_features(
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all features, optionally filtered by category."""
    query = db.query(Feature)
    if category:
        query = query.filter(Feature.category == category)
    features = query.all()
    if not features:
        raise HTTPException(status_code=404, detail="No features found")
    return features

@router.get("/features/{feature_name}", response_model=FeatureSchema)
async def get_feature(feature_name: str, db: Session = Depends(get_db)):
    """Get a specific feature by name."""
    feature = db.query(Feature).filter(Feature.name == feature_name).first()
    if not feature:
        raise HTTPException(status_code=404, detail=f"Feature not found: {feature_name}")
    return feature


@router.get("/sources")
async def get_sources():
    """Get public source metadata and caveats for the Slate data."""
    return _load_sources()
