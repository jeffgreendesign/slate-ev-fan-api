# API Endpoints

This section details all the available endpoints in the Slate EV Truck API.

## Root Endpoint

### GET /

Returns the main vehicle information.

**Parameters**: None

**Response**:

```json
{
  "id": 1,
  "model": "Slate EV Truck",
  "manufacturer": "Slate Motors",
  "vehicle_type": "Pickup",
  "production_start": "2027",
  "assembly_location": "Detroit, MI",
  "created_at": "2023-10-15T12:00:00",
  "updated_at": "2023-10-15T12:00:00",
  "dimensions": {
    "id": 1,
    "vehicle_id": 1,
    "length_mm": 5800,
    "width_mm": 2100,
    "height_mm": 1950,
    "wheelbase_mm": 3800,
    "bed_length_mm": 1800
  },
  "performance": {
    "id": 1,
    "vehicle_id": 1,
    "acceleration_0_60": 3.5,
    "top_speed_kmh": 180,
    "fuel_economy_mpge": 85
  },
  "powertrain": {
    "id": 1,
    "vehicle_id": 1,
    "motor_type": "Permanent Magnet Synchronous",
    "drive_type": "All-Wheel Drive",
    "power_output_hp": 500,
    "torque_nm": 800
  },
  "battery": {
    "id": 1,
    "vehicle_id": 1,
    "standard_capacity_kwh": 100.0,
    "optional_capacity_kwh": 150.0,
    "standard_range_km": 480,
    "optional_range_km": 720
  },
  "charging": {
    "id": 1,
    "vehicle_id": 1,
    "port_type": "CCS",
    "onboard_charger_kw": 11.5,
    "level1_charging_time_hours": 36.0,
    "level2_charging_time_hours": 10.0,
    "dc_fast_charging_time_minutes": 45
  },
  "features": [
    {
      "id": 1,
      "vehicle_id": 1,
      "name": "Advanced Driver Assistance",
      "description": "Includes adaptive cruise control, lane keeping assist, and automatic emergency braking",
      "category": "Safety",
      "is_optional": false,
      "price": null
    },
    {
      "id": 2,
      "vehicle_id": 1,
      "name": "Fast Charging",
      "description": "Supports DC fast charging up to 250kW",
      "category": "Charging",
      "is_optional": false,
      "price": null
    }
  ],
  "pricing": {
    "id": 1,
    "vehicle_id": 1,
    "base_price": 45000.0,
    "federal_tax_credit": 7500.0,
    "final_price": 37500.0,
    "reservation_deposit": 1000.0
  }
}
```

**Status Codes**:

- `200 OK`: Success
- `404 Not Found`: Vehicle not found

## Features

### GET /features

Retrieves all features of the Slate EV truck, optionally filtered by category.

**Parameters**:

| Name     | Type   | In    | Description                            |
| -------- | ------ | ----- | -------------------------------------- |
| category | string | query | (Optional) Filter features by category |

**Response**:

```json
[
  {
    "id": 1,
    "vehicle_id": 1,
    "name": "Advanced Driver Assistance",
    "description": "Includes adaptive cruise control, lane keeping assist, and automatic emergency braking",
    "category": "Safety",
    "is_optional": false,
    "price": null
  },
  {
    "id": 2,
    "vehicle_id": 1,
    "name": "Fast Charging",
    "description": "Supports DC fast charging up to 250kW",
    "category": "Charging",
    "is_optional": false,
    "price": null
  }
]
```

**Status Codes**:

- `200 OK`: Success
- `404 Not Found`: No features found

### GET /features/{feature_name}

Retrieves details of a specific feature by name.

**Parameters**:

| Name         | Type   | In   | Description         |
| ------------ | ------ | ---- | ------------------- |
| feature_name | string | path | Name of the feature |

**Response**:

```json
{
  "id": 1,
  "vehicle_id": 1,
  "name": "Advanced Driver Assistance",
  "description": "Includes adaptive cruise control, lane keeping assist, and automatic emergency braking",
  "category": "Safety",
  "is_optional": false,
  "price": null
}
```

**Status Codes**:

- `200 OK`: Success
- `404 Not Found`: Feature not found

## Examples

### Retrieving Vehicle Information

```bash
curl -X GET "http://localhost:8000/"
```

### Retrieving All Features

```bash
curl -X GET "http://localhost:8000/features"
```

### Filtering Features by Category

```bash
curl -X GET "http://localhost:8000/features?category=Safety"
```

### Retrieving a Specific Feature

```bash
curl -X GET "http://localhost:8000/features/Advanced%20Driver%20Assistance"
```
