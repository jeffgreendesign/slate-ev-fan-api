# API Endpoints

This section details all the available endpoints in the Slate EV Truck API.

## Root Endpoint

### GET /

Returns a welcome message to confirm the API is working.

**Parameters**: None

**Response**:

```json
{
  "message": "Welcome to the Slate EV Truck API"
}
```

**Status Codes**:

- `200 OK`: Success

## Vehicle Information

### GET /vehicles

Retrieves all vehicle information including specifications.

**Parameters**: None

**Response**:

```json
[
  {
    "id": 1,
    "name": "Slate EV Truck",
    "year": 2027,
    "specifications": {
      "battery_capacity": "150 kWh",
      "range": "300 miles",
      "horsepower": 500,
      "torque": 600,
      "payload_capacity": "2,000 lbs",
      "towing_capacity": "10,000 lbs",
      "price": "Starting at $45,000"
    }
  }
]
```

**Status Codes**:

- `200 OK`: Success
- `500 Internal Server Error`: Server error

## Features

### GET /features

Retrieves all features of the Slate EV truck.

**Parameters**:

| Name     | Type   | In    | Description                            |
| -------- | ------ | ----- | -------------------------------------- |
| category | string | query | (Optional) Filter features by category |

**Response**:

```json
[
  {
    "id": 1,
    "name": "Advanced Driver Assistance",
    "description": "Includes adaptive cruise control, lane keeping assist, and automatic emergency braking",
    "category": "Safety"
  },
  {
    "id": 2,
    "name": "Fast Charging",
    "description": "Supports DC fast charging up to 250kW for quick recharging on the go",
    "category": "Charging"
  }
]
```

**Status Codes**:

- `200 OK`: Success
- `400 Bad Request`: Invalid query parameter
- `500 Internal Server Error`: Server error

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
  "name": "Advanced Driver Assistance",
  "description": "Includes adaptive cruise control, lane keeping assist, and automatic emergency braking",
  "category": "Safety"
}
```

**Status Codes**:

- `200 OK`: Success
- `404 Not Found`: Feature not found
- `500 Internal Server Error`: Server error

## Examples

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
