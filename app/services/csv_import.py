import csv
import logging
from pathlib import Path
from typing import NamedTuple

from sqlalchemy.orm import Session
from app.models.vehicle import (
    Vehicle, Dimensions, Performance, Powertrain,
    Battery, Charging, Feature, Pricing, Capacity
)

logger = logging.getLogger(__name__)


class ImportResult(NamedTuple):
    vehicle: Vehicle
    imported: int
    skipped: int
    total: int

# Per-category maps of CSV "Specification" -> (target attribute, converter).
# Adding a spec to the CSV only requires an entry here.
_SPEC_MAP = {
    'Dimensions': {
        'Length': ('length_mm', float),
        'Width': ('width_mm', float),
        'Height': ('height_mm', float),
        'Wheelbase': ('wheelbase_mm', float),
        'Bed Length': ('bed_length_mm', float),
    },
    'Performance': {
        '0-60 mph': ('acceleration_0_60', float),
        'Top Speed': ('top_speed_kmh', int),
        'Fuel Economy': ('fuel_economy_mpge', int),
    },
    'Powertrain': {
        'Motor Type': ('motor_type', str),
        'Drive Type': ('drive_type', str),
        'Power Output': ('power_output_hp', int),
        'Torque': ('torque_nm', int),
    },
    'Battery': {
        'Standard Capacity': ('standard_capacity_kwh', float),
        'Optional Capacity': ('optional_capacity_kwh', float),
        'Standard Range': ('standard_range_km', int),
        'Optional Range': ('optional_range_km', int),
        'Usable Capacity': ('usable_capacity_kwh', float),
        'Chemistry': ('chemistry', str),
    },
    'Charging': {
        'Port Type': ('port_type', str),
        'Onboard Charger': ('onboard_charger_kw', float),
        'Level 1 Time': ('level1_charging_time_hours', float),
        'Level 2 Time': ('level2_charging_time_hours', float),
        'DC Fast Charging Time': ('dc_fast_charging_time_minutes', int),
    },
    'Pricing': {
        'Base Price': ('base_price', float),
        'Federal Tax Credit': ('federal_tax_credit', float),
        'Final Price': ('final_price', float),
        'Reservation Deposit': ('reservation_deposit', float),
        'Preorder Deposit': ('preorder_deposit', float),
    },
    'Capacity': {
        'Base Curb Weight': ('curb_weight_kg', float),
        'GVWR': ('gvwr_kg', float),
        'Max Payload': ('max_payload_kg', float),
        'Max Towing': ('max_towing_kg', float),
        'Frunk Volume': ('frunk_volume_l', float),
        'Bed Volume': ('bed_volume_l', float),
        'Cargo Space': ('cargo_volume_l', float),
    },
}

# Which vehicle relationship each category writes to.
_CATEGORY_TARGET = {
    'Dimensions': 'dimensions',
    'Performance': 'performance',
    'Powertrain': 'powertrain',
    'Battery': 'battery',
    'Charging': 'charging',
    'Pricing': 'pricing',
    'Capacity': 'capacity',
}

_BASIC_FIELDS = {
    'Model': 'model',
    'Manufacturer': 'manufacturer',
    'Vehicle Type': 'vehicle_type',
    'Production Start': 'production_start',
    'Assembly Location': 'assembly_location',
}


def import_csv_data(db: Session, csv_path: Path):
    """Import data from CSV file into database.

    Rows are processed individually: a malformed row is logged and skipped
    rather than aborting the import, so one bad value cannot silently
    truncate everything after it. Returns an ImportResult so callers can
    verify completeness (e.g. assert skipped == 0) instead of trusting that
    a returned vehicle implies every row landed.

    Does not commit. The caller decides the transaction boundary — e.g.
    main.py's _sync_csv_data() commits this together with clearing old data
    and recording the new CSV fingerprint, so a failure partway through
    can't leave the database with new data but stale bookkeeping.
    """
    with open(csv_path, 'r', encoding='utf-8', newline='') as file:
        rows = list(csv.DictReader(file))

    # First pass: the Basic category defines the vehicle itself.
    vehicle_data = {}
    for row in rows:
        if row.get('Category') != 'Basic':
            continue
        attr = _BASIC_FIELDS.get(row.get('Specification'))
        if attr:
            vehicle_data[attr] = row.get('Value')

    missing = [f for f in ('model', 'manufacturer', 'vehicle_type') if not vehicle_data.get(f)]
    if missing:
        raise ValueError(f"CSV is missing required Basic rows: {', '.join(missing)}")

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
    vehicle.capacity = Capacity(vehicle_id=vehicle.id)

    # Second pass: every other category.
    imported = 0
    skipped = 0
    for line_no, row in enumerate(rows, start=2):  # start=2 accounts for the header
        category = row.get('Category')
        spec = row.get('Specification')
        value = row.get('Value')

        if category == 'Basic':
            if spec not in _BASIC_FIELDS:
                logger.warning("Row %d: unknown Basic specification %r, skipping", line_no, spec)
                skipped += 1
            else:
                imported += 1
            continue

        try:
            if category == 'Feature':
                if not spec:
                    logger.warning("Row %d: feature has no name, skipping", line_no)
                    skipped += 1
                    continue
                is_optional = (row.get('Optional') or '').lower() == 'yes'
                db.add(Feature(
                    vehicle_id=vehicle.id,
                    name=spec,
                    description=value,
                    category=row.get('Additional Info'),
                    is_optional=is_optional,
                ))
                imported += 1
                continue

            target_attr = _CATEGORY_TARGET.get(category)
            if target_attr is None:
                logger.warning("Row %d: unknown category %r, skipping", line_no, category)
                skipped += 1
                continue

            field = _SPEC_MAP[category].get(spec)
            if field is None:
                logger.warning(
                    "Row %d: unknown specification %r for category %r, skipping",
                    line_no, spec, category,
                )
                skipped += 1
                continue

            attr_name, converter = field
            if value is None or value == '':
                logger.warning(
                    "Row %d: empty value for %s/%s, leaving as null", line_no, category, spec
                )
                skipped += 1
                continue

            setattr(getattr(vehicle, target_attr), attr_name, converter(value))
            imported += 1

        except (ValueError, TypeError, KeyError, AttributeError) as exc:
            logger.warning(
                "Row %d: could not import %s/%s (value=%r): %s",
                line_no, category, spec, value, exc,
            )
            skipped += 1

    db.flush()
    logger.info(
        "CSV import complete: %d rows imported, %d skipped, out of %d total",
        imported, skipped, len(rows),
    )
    return ImportResult(vehicle=vehicle, imported=imported, skipped=skipped, total=len(rows))
