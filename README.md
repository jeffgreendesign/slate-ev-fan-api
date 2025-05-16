# Slate EV Truck API

A FastAPI-based REST API that provides information about the Slate EV truck, including specifications, features, and other relevant details. The API includes Swagger UI documentation for easy testing and exploration.

## Features

- RESTful API endpoints for truck specifications and features
- Interactive API documentation with Swagger UI
- Data validation using Pydantic models
- Category-based feature filtering
- Detailed error handling
- SQLite database for data persistence
- CSV data import functionality
- Environment variable configuration

## Prerequisites

- Python 3.11 (required - other versions may have compatibility issues)
- pip (Python package installer)
- Virtual environment (recommended)

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd slate-ev-fan-api
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

4. Create a `.env` file in the project root (optional):

```bash
cp .env.example .env  # If .env.example exists
```

5. Run the API:

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

### 2. Vehicle Information

- **URL**: `/vehicles`
- **Method**: GET
- **Description**: Get all vehicle information
- **Response**: Array of vehicle objects with specifications and features

### 3. Features List

- **URL**: `/features`
- **Method**: GET
- **Description**: Get all features of the Slate EV truck
- **Query Parameters**:
  - `category` (optional): Filter features by category (e.g., "Safety", "Technology", "Charging")
- **Response**: Array of features

### 4. Specific Feature

- **URL**: `/features/{feature_name}`
- **Method**: GET
- **Description**: Get details of a specific feature
- **URL Parameters**:
  - `feature_name`: Name of the feature to retrieve
- **Response**: Feature details

## Project Structure

```
slate-ev-fan-api/
├── app/
│   ├── api/
│   │   └── endpoints.py    # API route definitions
│   ├── models/
│   │   └── models.py      # Pydantic models
│   ├── services/
│   │   └── csv_import.py  # CSV data import service
│   └── database.py        # Database configuration
├── data/
│   └── slate.csv         # Vehicle specifications data
├── main.py               # Main FastAPI application
├── requirements.txt      # Project dependencies
├── .env.example         # Example environment variables
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation
```

## Data Management

The project uses SQLite for data storage and includes functionality to import data from CSV files. The data directory contains the source CSV file with vehicle specifications.

## Dependencies

- FastAPI: Web framework for building APIs
- Uvicorn: ASGI server for running the API
- Pydantic: Data validation and settings management
- SQLAlchemy: SQL toolkit and ORM
- python-dotenv: Environment variable management

## Development

### Environment Variables

Create a `.env` file in the project root with the following variables (if needed):

```env
DATABASE_URL=sqlite:///./slate.db
```

### Database

The application uses SQLite as its database. The database file is created automatically on first run and is stored in the project root directory.

### Data Import

The application automatically imports data from the CSV file on startup. The CSV file should be placed in the `data/` directory.

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
