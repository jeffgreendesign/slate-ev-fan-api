# Slate EV Truck API Documentation

[![Netlify Status](https://api.netlify.com/api/v1/badges/9a67d4ca-a675-4c4b-ace4-26453b4bc15d/deploy-status)](https://app.netlify.com/projects/cool-baklava-79da84/deploys)

Welcome to the official documentation for the Slate EV Truck API. This API provides information about the Slate EV truck, including specifications, features, and other relevant details.

**Live Documentation URL**: [https://cool-baklava-79da84.netlify.app/](https://cool-baklava-79da84.netlify.app/)

## About the API

The Slate EV Truck API is a FastAPI-based REST API that makes it easy to:

- Retrieve detailed vehicle specifications
- Access feature information by category
- Get comprehensive information about the Slate EV truck

## Key Features

- **RESTful API endpoints** for truck specifications and features
- **Interactive documentation** with Swagger UI
- **Data validation** using Pydantic models
- **Category-based filtering** for features
- **SQLite database** for data persistence
- **CSV data import** functionality
- **Environment variable** configuration

## Getting Started

To get started with the API, visit the [Getting Started](guides/getting-started.md) guide.

## API Reference

For detailed information about the API endpoints, see the [API Overview](api/overview.md) and [Endpoints](api/endpoints.md) documentation.

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
└── requirements.txt      # Project dependencies
```

## Contributing

For information on how to contribute to the API, see the [Contributing](development/contributing.md) guide.
