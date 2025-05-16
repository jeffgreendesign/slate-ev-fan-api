from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Base schemas
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

# Create schemas
class DimensionsCreate(DimensionsBase):
    pass

class PerformanceCreate(PerformanceBase):
    pass

class PowertrainCreate(PowertrainBase):
    pass

class BatteryCreate(BatteryBase):
    pass

class ChargingCreate(ChargingBase):
    pass

class FeatureCreate(FeatureBase):
    pass

class PricingCreate(PricingBase):
    pass

class VehicleCreate(BaseModel):
    model: str
    manufacturer: str
    vehicle_type: str
    production_start: Optional[str] = None
    assembly_location: Optional[str] = None
    dimensions: Optional[DimensionsCreate] = None
    performance: Optional[PerformanceCreate] = None
    powertrain: Optional[PowertrainCreate] = None
    battery: Optional[BatteryCreate] = None
    charging: Optional[ChargingCreate] = None
    features: Optional[List[FeatureCreate]] = None
    pricing: Optional[PricingCreate] = None

# Response schemas
class Dimensions(DimensionsBase):
    id: int
    vehicle_id: int

    class Config:
        from_attributes = True

class Performance(PerformanceBase):
    id: int
    vehicle_id: int

    class Config:
        from_attributes = True

class Powertrain(PowertrainBase):
    id: int
    vehicle_id: int

    class Config:
        from_attributes = True

class Battery(BatteryBase):
    id: int
    vehicle_id: int

    class Config:
        from_attributes = True

class Charging(ChargingBase):
    id: int
    vehicle_id: int

    class Config:
        from_attributes = True

class Feature(FeatureBase):
    id: int
    vehicle_id: int

    class Config:
        from_attributes = True

class Pricing(PricingBase):
    id: int
    vehicle_id: int

    class Config:
        from_attributes = True

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