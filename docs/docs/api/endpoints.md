# API Endpoints

Base path: `/api/v1`

This is an unofficial fan API. Vehicle specs are compiled from public sources and remain preproduction/projected unless a field explicitly says otherwise.

## GET `/api/v1/`

Returns the main Slate Truck record imported from `data/slate.csv`.

Important current caveats:

- Model status: preproduction
- Production start: Q4 2026, first deliveries expected Q4 2026
- Range: 205 mi is Slate-estimated and is **not** a final EPA rating
- Pricing: base price announced 2026-06-24; excludes destination, taxes, title and registration
- The `$7,500` federal tax credit was eliminated and is recorded as `0`, not `null`

!!! note "Battery fields"
    Slate consolidated to a single 65 kWh LFP pack in June 2026. The
    `optional_capacity_kwh` and `optional_range_km` fields are retained and
    marked deprecated in the OpenAPI schema; they now return `null` rather
    than being removed, so existing consumers keep working.

Selected response fields:

```json
{
  "model": "Slate Truck",
  "manufacturer": "Slate Auto",
  "vehicle_type": "Preproduction electric pickup with SUV accessory conversion option",
  "production_start": "Q4 2026",
  "assembly_location": "Warsaw, Indiana, USA",
  "dimensions": {
    "length_mm": 4434.84,
    "width_mm": 1793.24,
    "height_mm": 1760.22,
    "wheelbase_mm": 2766.06,
    "bed_length_mm": 1524.0
  },
  "powertrain": {
    "motor_type": "135 kW permanent-magnet synchronous motor",
    "drive_type": "Rear-wheel drive",
    "power_output_hp": 181,
    "torque_nm": 264
  },
  "battery": {
    "standard_capacity_kwh": 65.0,
    "standard_range_km": 330,
    "usable_capacity_kwh": 63.0,
    "chemistry": "LFP",
    "optional_capacity_kwh": null,
    "optional_range_km": null
  },
  "charging": {
    "port_type": "NACS",
    "onboard_charger_kw": 11.0,
    "level1_charging_time_hours": 17.0,
    "level2_charging_time_hours": 4.0,
    "dc_fast_charging_time_minutes": 30
  },
  "capacity": {
    "curb_weight_kg": 1836.0,
    "gvwr_kg": 2580.0,
    "max_payload_kg": 703.0,
    "max_towing_kg": 907.0,
    "frunk_volume_l": 198.0,
    "bed_volume_l": 994.0,
    "cargo_volume_l": 963.0
  },
  "pricing": {
    "base_price": 24950.0,
    "federal_tax_credit": 0.0,
    "final_price": 24950.0,
    "reservation_deposit": 50.0,
    "preorder_deposit": 300.0
  }
}
```

## GET `/api/v1/features`

Returns all imported features. Supports optional exact category filtering.
Returns an empty array (`200`), not `404`, when no feature matches.

Example:

```bash
curl "http://localhost:8000/api/v1/features?category=Charging"
```

## GET `/api/v1/features/{feature_name}`

Returns one feature by exact feature name.

Example:

```bash
curl "http://localhost:8000/api/v1/features/NACS%20Charging"
```

## GET `/api/v1/sources`

Returns source metadata, caveats, and known unknowns used for the current data refresh.

Example:

```bash
curl "http://localhost:8000/api/v1/sources"
```

Selected response fields:

```json
{
  "official_affiliation": false,
  "last_reviewed": "2026-06-08",
  "status": "preproduction",
  "disclaimer": "Unofficial fan API data compiled from public sources...",
  "primary_sources": [
    {
      "label": "Slate Auto FAQ",
      "url": "https://www.slate.auto/en/faq"
    }
  ],
  "known_unknowns": [
    "Final MSRP/base price",
    "Final EPA-certified range and MPGe"
  ]
}
```
