import csv
from pathlib import Path
from sqlalchemy.orm import Session
from app.models.vehicle import (
    Vehicle, Dimensions, Performance, Powertrain,
    Battery, Charging, Feature, Pricing
)

def import_csv_data(db: Session, csv_path: Path):
    """Import data from CSV file into database."""
    with open(csv_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        
        # Create vehicle record
        vehicle_data = {}
        for row in csv_reader:
            category = row['Category']
            spec = row['Specification']
            value = row['Value']
            unit = row['Unit']
            is_optional = row['Optional'].lower() == 'yes' if row['Optional'] else False
            
            if category == 'Basic':
                if spec == 'Model':
                    vehicle_data['model'] = value
                elif spec == 'Manufacturer':
                    vehicle_data['manufacturer'] = value
                elif spec == 'Vehicle Type':
                    vehicle_data['vehicle_type'] = value
                elif spec == 'Production Start':
                    vehicle_data['production_start'] = value
                elif spec == 'Assembly Location':
                    vehicle_data['assembly_location'] = value
        
        # Create vehicle
        vehicle = Vehicle(**vehicle_data)
        db.add(vehicle)
        db.flush()  # Get the vehicle ID
        
        # Initialize related objects
        vehicle.dimensions = Dimensions(vehicle_id=vehicle.id)
        vehicle.performance = Performance(vehicle_id=vehicle.id)
        vehicle.powertrain = Powertrain(vehicle_id=vehicle.id)
        vehicle.battery = Battery(vehicle_id=vehicle.id)
        vehicle.charging = Charging(vehicle_id=vehicle.id)
        vehicle.pricing = Pricing(vehicle_id=vehicle.id)
        
        # Reset file pointer
        file.seek(0)
        next(csv_reader)  # Skip header
        
        # Process other categories
        for row in csv_reader:
            category = row['Category']
            spec = row['Specification']
            value = row['Value']
            unit = row['Unit']
            is_optional = row['Optional'].lower() == 'yes' if row['Optional'] else False
            
            if category == 'Dimensions':
                if spec == 'Length':
                    vehicle.dimensions.length_mm = float(value)
                elif spec == 'Width':
                    vehicle.dimensions.width_mm = float(value)
                elif spec == 'Height':
                    vehicle.dimensions.height_mm = float(value)
                elif spec == 'Wheelbase':
                    vehicle.dimensions.wheelbase_mm = float(value)
                elif spec == 'Bed Length':
                    vehicle.dimensions.bed_length_mm = float(value)
            
            elif category == 'Performance':
                if spec == '0-60 mph':
                    vehicle.performance.acceleration_0_60 = float(value)
                elif spec == 'Top Speed':
                    vehicle.performance.top_speed_kmh = int(value)
                elif spec == 'Fuel Economy':
                    vehicle.performance.fuel_economy_mpge = int(value)
            
            elif category == 'Powertrain':
                if spec == 'Motor Type':
                    vehicle.powertrain.motor_type = value
                elif spec == 'Drive Type':
                    vehicle.powertrain.drive_type = value
                elif spec == 'Power Output':
                    vehicle.powertrain.power_output_hp = int(value)
                elif spec == 'Torque':
                    vehicle.powertrain.torque_nm = int(value)
            
            elif category == 'Battery':
                if spec == 'Standard Capacity':
                    vehicle.battery.standard_capacity_kwh = float(value)
                elif spec == 'Optional Capacity':
                    vehicle.battery.optional_capacity_kwh = float(value)
                elif spec == 'Standard Range':
                    vehicle.battery.standard_range_km = int(value)
                elif spec == 'Optional Range':
                    vehicle.battery.optional_range_km = int(value)
            
            elif category == 'Charging':
                if spec == 'Port Type':
                    vehicle.charging.port_type = value
                elif spec == 'Onboard Charger':
                    vehicle.charging.onboard_charger_kw = float(value)
                elif spec == 'Level 1 Time':
                    vehicle.charging.level1_charging_time_hours = float(value)
                elif spec == 'Level 2 Time':
                    vehicle.charging.level2_charging_time_hours = float(value)
                elif spec == 'DC Fast Charging Time':
                    vehicle.charging.dc_fast_charging_time_minutes = int(value)
            
            elif category == 'Feature':
                feature = Feature(
                    vehicle_id=vehicle.id,
                    name=spec,
                    description=value,
                    category=row.get('Additional Info'),
                    is_optional=is_optional
                )
                db.add(feature)
            
            elif category == 'Pricing':
                if spec == 'Base Price':
                    vehicle.pricing.base_price = float(value)
                elif spec == 'Federal Tax Credit':
                    vehicle.pricing.federal_tax_credit = float(value)
                elif spec == 'Final Price':
                    vehicle.pricing.final_price = float(value)
                elif spec == 'Reservation Deposit':
                    vehicle.pricing.reservation_deposit = float(value)
        
        db.commit()
        return vehicle 