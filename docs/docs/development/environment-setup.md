# Development Environment Setup

This guide provides detailed instructions for setting up a development environment for the Slate EV Truck API.

## Development Prerequisites

- Python 3.11 (required - other versions may have compatibility issues)
- pip (Python package installer)
- Git
- A code editor or IDE (VS Code recommended)

## Setting Up the Development Environment

### 1. Clone the Repository

```bash
git clone <repository-url>
cd slate-ev-fan-api
```

### 2. Create a Virtual Environment

#### On macOS/Linux

```bash
python3.11 -m venv venv
source venv/bin/activate
```

#### On Windows

```bash
python3.11 -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### Development Dependencies

For development, you might want to install additional packages:

```bash
pip install pytest pytest-cov black isort flake8 mypy
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```
DATABASE_URL=sqlite:///./slate.db
ENVIRONMENT=development
DEBUG=True
```

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
├── tests/                # Test directory
│   ├── test_api/
│   ├── test_models/
│   └── test_services/
├── main.py               # Main FastAPI application
├── requirements.txt      # Project dependencies
└── README.md            # Project documentation
```

## Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=app

# Generate HTML coverage report
pytest --cov=app --cov-report=html
```

## Code Formatting and Linting

```bash
# Format code with Black
black app tests main.py

# Sort imports with isort
isort app tests main.py

# Run linting with flake8
flake8 app tests main.py

# Run type checking with mypy
mypy app tests main.py
```

## Database Management

The API uses SQLite for development. The database file is created automatically on first run.

### Working with the Database

- The database file is created at `slate.db` in the project root
- You can use SQLite tools to inspect the database
- To reset the database, simply delete the `slate.db` file

### Data Import

Data is imported from CSV on startup:

1. Place your CSV file in the `data/` directory
2. The CSV file should be named `slate.csv`
3. Run the application to import the data

## Development Workflow

1. Create a new branch for your feature
2. Implement your changes
3. Write tests for your changes
4. Run the test suite to ensure everything passes
5. Format and lint your code
6. Commit your changes
7. Push to your fork/branch
8. Create a pull request

## Troubleshooting Common Issues

### Database Issues

If you encounter database issues:

1. Delete the database file: `rm slate.db`
2. Restart the application

### Import Errors

If you encounter import errors:

1. Check your Python version (`python --version`)
2. Ensure your virtual environment is activated
3. Reinstall dependencies: `pip install -r requirements.txt`

### Environment Variable Issues

If environment variables aren't being loaded:

1. Check that your `.env` file is in the project root
2. Ensure the file has the correct permissions
3. Try setting the variables manually in your terminal
