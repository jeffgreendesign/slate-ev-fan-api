import hashlib
import logging
import re
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from sqlalchemy import inspect, text

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

_SAFE_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _csv_fingerprint(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sync_schema(engine) -> None:
    """Add columns present in the ORM models but missing from an existing DB file.

    Base.metadata.create_all() only creates tables that don't exist yet; it
    never alters an existing table's columns. Without this, a slate.db
    persisted from before a model change (e.g. Battery.chemistry,
    Pricing.preorder_deposit) would keep its old schema and every query
    touching the new column would fail at runtime with "no such column".
    Only additive, nullable columns are handled — sufficient for this
    project's forward-only, CSV-driven model changes.
    """
    if engine.dialect.name != "sqlite":
        logger.warning("Schema auto-sync only supports SQLite; skipping")
        return

    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())

    with engine.begin() as conn:
        for table in Base.metadata.sorted_tables:
            if table.name not in existing_tables:
                continue  # brand-new table; create_all() will handle it
            existing_columns = {col["name"] for col in inspector.get_columns(table.name)}
            for column in table.columns:
                if column.name in existing_columns:
                    continue
                # SQL has no parameter-binding syntax for identifiers (only
                # values), so table/column names can't go through bindparams.
                # Both come solely from our own ORM metadata, never from
                # user input, but they're validated anyway as defense in
                # depth against a future name containing SQL metacharacters.
                if not (_SAFE_IDENTIFIER.match(table.name) and _SAFE_IDENTIFIER.match(column.name)):
                    raise ValueError(f"Unsafe identifier in schema sync: {table.name}.{column.name}")
                col_type = column.type.compile(engine.dialect)
                ddl = f'ALTER TABLE "{table.name}" ADD COLUMN "{column.name}" {col_type}'  # ddl-identifiers-validated
                conn.execute(text(ddl))
                logger.info("Added missing column %s.%s", table.name, column.name)


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

    replacing = meta is not None or db.query(Vehicle).first()

    try:
        if replacing:
            logger.info("CSV changed — clearing existing data and re-importing")
            for model in _DATA_MODELS:
                db.query(model).delete()
            db.query(ImportMeta).delete()

        result = import_csv_data(db, CSV_PATH)
        if result.skipped:
            # Don't record this fingerprint as successfully imported — a
            # partial import must not be mistaken for the known-good state
            # on the next startup. Raising rolls back the whole attempt.
            raise ValueError(
                f"CSV import incomplete: {result.skipped} of {result.total} "
                f"row(s) skipped; see warnings above for details"
            )
        db.add(ImportMeta(csv_sha256=fingerprint))
        db.commit()
    except Exception:  # transactional-rollback-guard: always re-raised, never swallowed
        # Roll back the deletion too, so a bad replacement CSV can never
        # leave the app with no data at all.
        db.rollback()
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables and load CSV data before the app starts serving."""
    _sync_schema(engine)
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
