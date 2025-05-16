# Slate EV Truck API

A FastAPI-based REST API that provides information about the Slate EV truck, including specifications, features, and other relevant details. The API includes Swagger UI documentation for easy testing and exploration.

## Features

- RESTful API endpoints for truck specifications and features
- Interactive API documentation with Swagger UI
- Data validation using Pydantic models
- Category-based feature filtering
- Detailed error handling

## Prerequisites

- Python 3.11 or later
- pip (Python package installer)
- Virtual environment (recommended)

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd api-test-01
```

2. Create a virtual environment:

```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the API:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation (Swagger UI) will be available at `http://localhost:8000/docs`

## API Endpoints

### 1. Root Endpoint

- **URL**: `/`
- **Method**: GET
- **Description**: Welcome message
- **Response**:

```json
{
  "message": "Welcome to the Slate EV Truck API"
}
```

### 2. Truck Specifications

- **URL**: `/specs`
- **Method**: GET
- **Description**: Get detailed specifications of the Slate EV truck
- **Response**:

```json
{
  "model": "Slate EV Truck",
  "battery_capacity": "150 kWh",
  "range": "300 miles",
  "horsepower": 500,
  "torque": 600,
  "payload_capacity": "2,000 lbs",
  "towing_capacity": "10,000 lbs",
  "price": "Starting at $45,000"
}
```

### 3. Features List

- **URL**: `/features`
- **Method**: GET
- **Description**: Get all features of the Slate EV truck
- **Query Parameters**:
  - `category` (optional): Filter features by category (e.g., "Safety", "Technology", "Charging")
- **Response**: Array of features

```json
[
  {
    "name": "Advanced Driver Assistance",
    "description": "Includes adaptive cruise control, lane keeping assist, and automatic emergency braking",
    "category": "Safety"
  }
  // ... more features
]
```

### 4. Specific Feature

- **URL**: `/features/{feature_name}`
- **Method**: GET
- **Description**: Get details of a specific feature
- **URL Parameters**:
  - `feature_name`: Name of the feature to retrieve
- **Response**: Feature details

```json
{
  "name": "Advanced Driver Assistance",
  "description": "Includes adaptive cruise control, lane keeping assist, and automatic emergency braking",
  "category": "Safety"
}
```

## Testing the API

### Using Swagger UI (Recommended)

1. Open `http://localhost:8000/docs` in your browser
2. Click on any endpoint you want to test
3. Click the "Try it out" button
4. Fill in any required parameters
5. Click "Execute" to make the request
6. View the response in the browser

### Using curl

1. Test the root endpoint:

```bash
curl http://localhost:8000/
```

2. Get truck specifications:

```bash
curl http://localhost:8000/specs
```

3. Get all features:

```bash
curl http://localhost:8000/features
```

4. Get features by category:

```bash
curl http://localhost:8000/features?category=Safety
```

5. Get a specific feature:

```bash
curl http://localhost:8000/features/Advanced%20Driver%20Assistance
```

## Error Handling

The API includes proper error handling for common scenarios:

- 404 Not Found: When a requested feature or category doesn't exist
- 422 Unprocessable Entity: When request parameters are invalid
- 500 Internal Server Error: For unexpected server errors

## Project Structure

```
api-test-01/
├── main.py           # Main FastAPI application
├── requirements.txt  # Project dependencies
└── README.md        # Project documentation
```

## Dependencies

- FastAPI 0.88.0: Web framework for building APIs
- Uvicorn 0.20.0: ASGI server for running the API
- Pydantic 1.10.2: Data validation and settings management

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
