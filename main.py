import hashlib
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from app.api.endpoints import router as api_router
from app.core.config import settings
from app.db.session import engine, Base, SessionLocal
from app.models.vehicle import (
    Vehicle, Dimensions, Performance, Powertrain,
    Battery, Charging, Feature, Pricing, Capacity, ImportMeta
)
from app.services.csv_import import import_csv_data

logger = logging.getLogger(__name__)

CSV_PATH = Path("data/slate.csv")

# Child tables first so foreign keys stay satisfied during a reload.
_DATA_MODELS = (
    Dimensions, Performance, Powertrain, Battery,
    Charging, Feature, Pricing, Capacity, Vehicle,
)


def _csv_fingerprint(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sync_csv_data(db) -> None:
    """Import the CSV if it is new or has changed since the last import."""
    if not CSV_PATH.exists():
        logger.warning("%s not found — skipping data import", CSV_PATH)
        return

    fingerprint = _csv_fingerprint(CSV_PATH)
    meta = db.query(ImportMeta).first()

    if meta is not None and meta.csv_sha256 == fingerprint and db.query(Vehicle).first():
        logger.info("CSV unchanged since last import — skipping")
        return

    if meta is not None or db.query(Vehicle).first():
        logger.info("CSV changed — clearing existing data and re-importing")
        for model in _DATA_MODELS:
            db.query(model).delete()
        db.query(ImportMeta).delete()
        db.commit()

    import_csv_data(db, CSV_PATH)
    db.add(ImportMeta(csv_sha256=fingerprint))
    db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables and load CSV data before the app starts serving."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        _sync_csv_data(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API for information about the Slate EV truck",
    lifespan=lifespan,
)


@app.get("/", tags=["meta"])
async def root():
    """Service descriptor pointing at the versioned API."""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "api_base": settings.API_V1_STR,
        "docs": "/docs",
        "openapi": "/openapi.json",
    }


# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)
