from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Slate EV Truck API",
    description="API for information about the Slate EV truck",
    version="1.0.0"
)

class TruckSpecs(BaseModel):
    model: str
    battery_capacity: str
    range: str
    horsepower: int
    torque: int
    payload_capacity: str
    towing_capacity: str
    price: Optional[str] = None

class Feature(BaseModel):
    name: str
    description: str
    category: str

# Sample data
truck_specs = TruckSpecs(
    model="Slate EV Truck",
    battery_capacity="150 kWh",
    range="300 miles",
    horsepower=500,
    torque=600,
    payload_capacity="2,000 lbs",
    towing_capacity="10,000 lbs",
    price="Starting at $45,000"
)

features = [
    Feature(
        name="Advanced Driver Assistance",
        description="Includes adaptive cruise control, lane keeping assist, and automatic emergency braking",
        category="Safety"
    ),
    Feature(
        name="Large Touchscreen Display",
        description="15-inch touchscreen with navigation and vehicle controls",
        category="Technology"
    ),
    Feature(
        name="Fast Charging",
        description="Supports DC fast charging up to 250 kW",
        category="Charging"
    )
]

@app.get("/")
async def root():
    return {"message": "Welcome to the Slate EV Truck API"}

@app.get("/specs", response_model=TruckSpecs)
async def get_specs():
    return truck_specs

@app.get("/features", response_model=List[Feature])
async def get_features(category: Optional[str] = None):
    if category:
        filtered_features = [f for f in features if f.category.lower() == category.lower()]
        if not filtered_features:
            raise HTTPException(status_code=404, detail=f"No features found in category: {category}")
        return filtered_features
    return features

@app.get("/features/{feature_name}", response_model=Feature)
async def get_feature(feature_name: str):
    for feature in features:
        if feature.name.lower() == feature_name.lower():
            return feature
    raise HTTPException(status_code=404, detail=f"Feature not found: {feature_name}") 