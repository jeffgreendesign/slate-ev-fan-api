# Getting Started

This guide will help you get started with the Slate EV Truck API. Follow these steps to set up and run the API locally.

## Prerequisites

Before you begin, ensure you have the following:

- Python 3.11 (required - other versions may have compatibility issues)
- pip (Python package installer)
- Git (for cloning the repository)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd slate-ev-fan-api
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to avoid conflicts with other Python projects.

On macOS/Linux:

```bash
python3.11 -m venv venv
source venv/bin/activate
```

On Windows:

```bash
python3.11 -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables (Optional)

Create a `.env` file in the project root:

```bash
cp .env.example .env  # If .env.example exists
```

Or manually create a `.env` file with the following content:

```
DATABASE_URL=sqlite:///./slate.db
```

## Running the API

Start the API server with:

```bash
uvicorn main:app --reload
```

This will start the development server at `http://localhost:8000`.

## Accessing the API

Once the server is running, you can:

- View the API documentation at `http://localhost:8000/docs`
- Try the alternative documentation UI at `http://localhost:8000/redoc`
- Make direct requests to the API endpoints

## Making API Requests

### Using cURL

Get all vehicles:

```bash
curl -X GET "http://localhost:8000/vehicles"
```

Get all features:

```bash
curl -X GET "http://localhost:8000/features"
```

Filter features by category:

```bash
curl -X GET "http://localhost:8000/features?category=Safety"
```

### Using Python

```python
import requests

# Get all vehicles
response = requests.get("http://localhost:8000/vehicles")
vehicles = response.json()
print(vehicles)

# Get features with a specific category
response = requests.get("http://localhost:8000/features", params={"category": "Safety"})
features = response.json()
print(features)
```

### Using JavaScript

```javascript
// Get all vehicles
fetch("http://localhost:8000/vehicles")
  .then((response) => response.json())
  .then((data) => console.log(data));

// Get features with a specific category
fetch("http://localhost:8000/features?category=Safety")
  .then((response) => response.json())
  .then((data) => console.log(data));
```

## Next Steps

After setting up and running the API, you might want to:

1. Explore the [API endpoints](../api/endpoints.md) in detail
2. Learn about the [data models](../api/models.md)
3. Read the [deployment guide](deployment.md) to deploy the API
4. Check out the [environment setup](../development/environment-setup.md) for development
