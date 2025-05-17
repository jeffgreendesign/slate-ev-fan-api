# Data Models

This section describes the data models used in the Slate EV Truck API.

## Database Models

The API uses SQLAlchemy ORM to interact with the database. Here are the database models:

### Vehicle

```python
class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String, nullable=False)
    manufacturer = Column(String, nullable=False)
    vehicle_type = Column(String, nullable=False)
    production_start = Column(String)
    assembly_location = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    dimensions = relationship("Dimensions", back_populates="vehicle", uselist=False)
    performance = relationship("Performance", back_populates="vehicle", uselist=False)
    powertrain = relationship("Powertrain", back_populates="vehicle", uselist=False)
    battery = relationship("Battery", back_populates="vehicle", uselist=False)
    charging = relationship("Charging", back_populates="vehicle", uselist=False)
    features = relationship("Feature", back_populates="vehicle")
    pricing = relationship("Pricing", back_populates="vehicle", uselist=False)
```

### Dimensions

```python
class Dimensions(Base):
    __tablename__ = "dimensions"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    length_mm = Column(Float)
    width_mm = Column(Float)
    height_mm = Column(Float)
    wheelbase_mm = Column(Float)
    bed_length_mm = Column(Float)

    vehicle = relationship("Vehicle", back_populates="dimensions")
```

### Performance

```python
class Performance(Base):
    __tablename__ = "performance"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    acceleration_0_60 = Column(Float)
    top_speed_kmh = Column(Integer)
    fuel_economy_mpge = Column(Integer)

    vehicle = relationship("Vehicle", back_populates="performance")
```

### Powertrain

```python
class Powertrain(Base):
    __tablename__ = "powertrain"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    motor_type = Column(String)
    drive_type = Column(String)
    power_output_hp = Column(Integer)
    torque_nm = Column(Integer)

    vehicle = relationship("Vehicle", back_populates="powertrain")
```

### Battery

```python
class Battery(Base):
    __tablename__ = "battery"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    standard_capacity_kwh = Column(Float)
    optional_capacity_kwh = Column(Float)
    standard_range_km = Column(Integer)
    optional_range_km = Column(Integer)

    vehicle = relationship("Vehicle", back_populates="battery")
```

### Charging

```python
class Charging(Base):
    __tablename__ = "charging"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    port_type = Column(String)
    onboard_charger_kw = Column(Float)
    level1_charging_time_hours = Column(Float)
    level2_charging_time_hours = Column(Float)
    dc_fast_charging_time_minutes = Column(Integer)

    vehicle = relationship("Vehicle", back_populates="charging")
```

### Feature

```python
class Feature(Base):
    __tablename__ = "features"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    name = Column(String, nullable=False)
    description = Column(String)
    category = Column(String)
    is_optional = Column(Boolean, default=False)
    price = Column(Float)

    vehicle = relationship("Vehicle", back_populates="features")
```

### Pricing

```python
class Pricing(Base):
    __tablename__ = "pricing"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    base_price = Column(Float)
    federal_tax_credit = Column(Float)
    final_price = Column(Float)
    reservation_deposit = Column(Float)

    vehicle = relationship("Vehicle", back_populates="pricing")
```

## Pydantic Schemas

These schemas are used for request/response validation and serialization.

### Base Schemas

```python
class DimensionsBase(BaseModel):
    length_mm: Optional[float] = None
    width_mm: Optional[float] = None
    height_mm: Optional[float] = None
    wheelbase_mm: Optional[float] = None
    bed_length_mm: Optional[float] = None

class PerformanceBase(BaseModel):
    acceleration_0_60: Optional[float] = None
    top_speed_kmh: Optional[int] = None
    fuel_economy_mpge: Optional[int] = None

class PowertrainBase(BaseModel):
    motor_type: Optional[str] = None
    drive_type: Optional[str] = None
    power_output_hp: Optional[int] = None
    torque_nm: Optional[int] = None

class BatteryBase(BaseModel):
    standard_capacity_kwh: Optional[float] = None
    optional_capacity_kwh: Optional[float] = None
    standard_range_km: Optional[int] = None
    optional_range_km: Optional[int] = None

class ChargingBase(BaseModel):
    port_type: Optional[str] = None
    onboard_charger_kw: Optional[float] = None
    level1_charging_time_hours: Optional[float] = None
    level2_charging_time_hours: Optional[float] = None
    dc_fast_charging_time_minutes: Optional[int] = None

class FeatureBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    is_optional: bool = False
    price: Optional[float] = None

class PricingBase(BaseModel):
    base_price: Optional[float] = None
    federal_tax_credit: Optional[float] = None
    final_price: Optional[float] = None
    reservation_deposit: Optional[float] = None
```

### Response Schemas

```python
class Vehicle(BaseModel):
    id: int
    model: str
    manufacturer: str
    vehicle_type: str
    production_start: Optional[str] = None
    assembly_location: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    dimensions: Optional[Dimensions] = None
    performance: Optional[Performance] = None
    powertrain: Optional[Powertrain] = None
    battery: Optional[Battery] = None
    charging: Optional[Charging] = None
    features: List[Feature] = []
    pricing: Optional[Pricing] = None

    class Config:
        from_attributes = True
```

```python
class Feature(FeatureBase):
    id: int
    vehicle_id: int

    class Config:
        from_attributes = True
```
