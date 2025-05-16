from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

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

class Performance(Base):
    __tablename__ = "performance"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    acceleration_0_60 = Column(Float)
    top_speed_kmh = Column(Integer)
    fuel_economy_mpge = Column(Integer)

    vehicle = relationship("Vehicle", back_populates="performance")

class Powertrain(Base):
    __tablename__ = "powertrain"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    motor_type = Column(String)
    drive_type = Column(String)
    power_output_hp = Column(Integer)
    torque_nm = Column(Integer)

    vehicle = relationship("Vehicle", back_populates="powertrain")

class Battery(Base):
    __tablename__ = "battery"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    standard_capacity_kwh = Column(Float)
    optional_capacity_kwh = Column(Float)
    standard_range_km = Column(Integer)
    optional_range_km = Column(Integer)

    vehicle = relationship("Vehicle", back_populates="battery")

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

class Pricing(Base):
    __tablename__ = "pricing"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    base_price = Column(Float)
    federal_tax_credit = Column(Float)
    final_price = Column(Float)
    reservation_deposit = Column(Float)

    vehicle = relationship("Vehicle", back_populates="pricing") 