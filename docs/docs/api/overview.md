# API Overview

The Slate EV Truck API is designed to provide comprehensive information about the Slate EV truck. This section provides an overview of the API structure, authentication methods, and general usage guidelines.

## Base URL

All API requests should be made to the base URL:

```
http://localhost:8000
```

When deployed, this will be replaced with your production URL.

## Authentication

Currently, the API is open and doesn't require authentication. Future versions may implement authentication mechanisms for production use.

## Response Format

All responses are returned in JSON format. A typical successful response follows this structure:

```json
{
  "data": [
    // Response data here
  ],
  "meta": {
    "count": 1,
    "page": 1,
    "total_pages": 1
  }
}
```

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of a request:

| Status Code | Description                                             |
| ----------- | ------------------------------------------------------- |
| 200         | OK - The request was successful                         |
| 400         | Bad Request - The request was invalid                   |
| 404         | Not Found - The requested resource was not found        |
| 422         | Unprocessable Entity - Validation error                 |
| 500         | Internal Server Error - An error occurred on the server |

Error responses follow this structure:

```json
{
  "detail": "Error message here"
}
```

## Rate Limiting

Currently, there are no rate limits implemented. In production, rate limiting may be applied to prevent abuse.

## API Versioning

The current version of the API is v1. The version is not included in the URL path but may be in future iterations.

## Available Endpoints

The API provides the following main endpoints:

| Endpoint           | Method | Description                    |
| ------------------ | ------ | ------------------------------ |
| `/`                | GET    | Welcome message                |
| `/vehicles`        | GET    | Get all vehicle information    |
| `/features`        | GET    | Get all features               |
| `/features/{name}` | GET    | Get a specific feature by name |

For detailed information about each endpoint, see the [Endpoints](endpoints.md) documentation.
