# API Endpoints

Base path: `/api/v1`

This is an unofficial fan API. Vehicle specs are compiled from public sources and remain preproduction/projected unless a field explicitly says otherwise.

## GET `/api/v1/`

Returns the main Slate Truck record imported from `data/slate.csv`.

Important current caveats:

- Model status: preproduction
- Production start: late 2026 target
- Range: projected, not final EPA-rated range
- Pricing: final MSRP not announced; only the $50 refundable reservation deposit is treated as structured price data

Selected response fields:

```json
{
  "model": "Slate Truck",
  "manufacturer": "Slate Auto",
  "vehicle_type": "Preproduction electric pickup with SUV accessory conversion option",
  "production_start": "Late 2026 target",
  "assembly_location": "Warsaw",
  "dimensions": {
    "length_mm": 4434.84,
    "width_mm": 1793.24,
    "height_mm": 1760.22,
    "wheelbase_mm": 2766.06,
    "bed_length_mm": 1524.0
  },
  "battery": {
    "standard_capacity_kwh": 52.7,
    "optional_capacity_kwh": 84.3,
    "standard_range_km": 241,
    "optional_range_km": 386
  },
  "charging": {
    "port_type": "NACS",
    "onboard_charger_kw": 11.0,
    "level1_charging_time_hours": 11.0,
    "level2_charging_time_hours": 5.0,
    "dc_fast_charging_time_minutes": 30
  },
  "pricing": {
    "base_price": null,
    "federal_tax_credit": null,
    "final_price": null,
    "reservation_deposit": 50.0
  }
}
```

## GET `/api/v1/features`

Returns all imported features. Supports optional exact category filtering.

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
