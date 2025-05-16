# Data Models

This section describes the data models used in the Slate EV Truck API.

## Vehicle Model

The Vehicle model represents a vehicle with its specifications.

```python
class Vehicle(BaseModel):
    id: int
    name: str
    year: int
    specifications: dict
```

**Fields**:

| Field          | Type    | Description                              |
| -------------- | ------- | ---------------------------------------- |
| id             | integer | Unique identifier for the vehicle        |
| name           | string  | Name of the vehicle                      |
| year           | integer | Model year of the vehicle                |
| specifications | object  | Object containing vehicle specifications |

## Feature Model

The Feature model represents a feature of the Slate EV truck.

```python
class Feature(BaseModel):
    id: int
    name: str
    description: str
    category: str
```

**Fields**:

| Field       | Type    | Description                              |
| ----------- | ------- | ---------------------------------------- |
| id          | integer | Unique identifier for the feature        |
| name        | string  | Name of the feature                      |
| description | string  | Detailed description of the feature      |
| category    | string  | Category of the feature (e.g., "Safety") |

## Database Models

The API uses SQLAlchemy ORM to interact with the database. Here are the database models:

### VehicleModel

```python
class VehicleModel(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    year = Column(Integer)
    specifications = Column(JSON)
    features = relationship("FeatureModel", back_populates="vehicle")
```

### FeatureModel

```python
class FeatureModel(Base):
    __tablename__ = "features"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    category = Column(String, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    vehicle = relationship("VehicleModel", back_populates="features")
```

## Response Models

These models are used to structure API responses.

### VehicleResponse

```python
class VehicleResponse(BaseModel):
    id: int
    name: str
    year: int
    specifications: Dict[str, Any]
    features: List[FeatureResponse] = []

    class Config:
        orm_mode = True
```

### FeatureResponse

```python
class FeatureResponse(BaseModel):
    id: int
    name: str
    description: str
    category: str

    class Config:
        orm_mode = True
```

### ErrorResponse

```python
class ErrorResponse(BaseModel):
    detail: str
```
