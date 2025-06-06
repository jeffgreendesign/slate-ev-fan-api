# Slate EV Truck API

A FastAPI-based REST API that provides information about the Slate EV truck, including specifications, features, and other relevant details. The API includes Swagger UI documentation for easy testing and exploration.

[![Netlify Status](https://api.netlify.com/api/v1/badges/9a67d4ca-a675-4c4b-ace4-26453b4bc15d/deploy-status)](https://app.netlify.com/sites/cool-baklava-79da84/deploys)

## Documentation

**[View the full documentation](https://cool-baklava-79da84.netlify.app/)**

The complete documentation for this API is available at [https://cool-baklava-79da84.netlify.app/](https://cool-baklava-79da84.netlify.app/)

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
- **Description**: Get the main vehicle information
- **Response**: Vehicle object with specifications and features

### 2. Features List

- **URL**: `/features`
- **Method**: GET
- **Description**: Get all features of the Slate EV truck
- **Query Parameters**:
  - `category` (optional): Filter features by category (e.g., "Safety", "Technology", "Charging")
- **Response**: Array of features

### 3. Specific Feature

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
│   │   └── vehicle.py      # SQLAlchemy ORM models
│   ├── schemas/
│   │   └── vehicle.py      # Pydantic schemas
│   ├── services/
│   │   └── csv_import.py   # CSV data import service
│   └── db/
│       └── session.py      # Database configuration
├── data/
│   └── slate.csv          # Vehicle specifications data
├── docs/                  # Documentation site
│   ├── docs/              # Markdown documentation files
│   ├── mkdocs.yml         # MkDocs configuration
│   ├── netlify.toml       # Netlify configuration
│   └── requirements.txt   # Documentation dependencies
├── main.py                # Main FastAPI application
└── requirements.txt       # Project dependencies
```

## Data Models

The API uses SQLAlchemy ORM models for database interaction and Pydantic schemas for request/response validation. Key models include:

- Vehicle: Main vehicle information
- Dimensions: Vehicle dimensions
- Performance: Performance specifications
- Powertrain: Motor and drivetrain details
- Battery: Battery specifications
- Charging: Charging capabilities
- Feature: Vehicle features
- Pricing: Pricing information

For detailed model information, see the [API Models Documentation](https://cool-baklava-79da84.netlify.app/api/models/).

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

## Deployment

Here are the top 4 options for deploying your FastAPI application, ordered by ease of use and free tier availability:

### 1. Railway.app (Recommended)

[Railway.app](https://railway.app/) offers the simplest deployment process with a generous free tier:

1. Go to [Railway.app](https://railway.app/) and sign up with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Add environment variables:
   ```
   DATABASE_URL=sqlite:///./slate.db
   ENVIRONMENT=production
   ```

### 2. Render.com

[Render](https://render.com/) provides a simple deployment process with a free tier:

1. Sign up at [Render.com](https://render.com/)
2. Connect your GitHub repository
3. Create a new Web Service
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Environment Variables:
     ```
     DATABASE_URL=sqlite:///./slate.db
     ENVIRONMENT=production
     ```

### 3. PythonAnywhere

[PythonAnywhere](https://www.pythonanywhere.com/) is great for Python applications:

1. Sign up for a free account
2. Go to Web tab and create a new web app
3. Choose "FastAPI" as your framework
4. Upload your code or clone from GitHub
5. Configure your virtual environment and requirements

### 4. Fly.io

[Fly.io](https://fly.io/) offers a generous free tier with global deployment:

1. Install Fly CLI:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```
2. Sign up and login:
   ```bash
   fly auth signup
   fly auth login
   ```
3. Create a `fly.toml`:
   ```bash
   fly launch
   ```
4. Deploy:
   ```bash
   fly deploy
   ```

## Documentation Site

This project includes a comprehensive documentation site built with MkDocs and the Material theme. The documentation is automatically deployed to Netlify whenever changes are pushed to the main branch.

- **Live Documentation**: [https://cool-baklava-79da84.netlify.app/](https://cool-baklava-79da84.netlify.app/)
- **Deploy Status**: [![Netlify Status](https://api.netlify.com/api/v1/badges/9a67d4ca-a675-4c4b-ace4-26453b4bc15d/deploy-status)](https://app.netlify.com/sites/cool-baklava-79da84/deploys)

For more information about the documentation site, see the [Deployment Guide](https://cool-baklava-79da84.netlify.app/guides/deployment/).

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

For more detailed contribution guidelines, see the [Contributing Guide](https://cool-baklava-79da84.netlify.app/development/contributing/).

## License

This project is licensed under the MIT License - see the LICENSE file for details.
