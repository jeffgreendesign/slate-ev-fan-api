from fastapi import FastAPI
from app.core.config import settings
from app.api.endpoints import router as api_router
from app.db.session import engine, Base
from app.services.csv_import import import_csv_data
from pathlib import Path

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API for information about the Slate EV truck"
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    """Initialize the database with CSV data on startup."""
    from app.db.session import SessionLocal
    db = SessionLocal()
    try:
        # Check if we already have data
        from app.models.vehicle import Vehicle
        if not db.query(Vehicle).first():
            # Import CSV data
            csv_path = Path("data/slate.csv")
            if csv_path.exists():
                import_csv_data(db, csv_path)
    finally:
        db.close() 