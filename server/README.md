# OGCR API Mockup Server

A FastAPI implementation of the OGCR API Specification for testing and development purposes.

## Features

- Full implementation of OGCR API endpoints
- OpenAPI/Swagger documentation
- Request/response validation using Pydantic models
- CORS support for frontend integration
- Mock authentication system
- In-memory data storage for testing

## Quick Start

### Using Python

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

3. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Using Docker

1. Build the image:
```bash
docker build -t ogcr-api .
```

2. Run the container:
```bash
docker run -p 8000:8000 ogcr-api
```

## API Endpoints

### Projects
- `POST /projects` - Create a new project
- `GET /projects` - List projects with filtering
- `GET /projects/{id}` - Get project details
- `PUT /projects/{id}` - Update project (draft only)
- `POST /projects/{id}/submit` - Submit for approval
- `POST /projects/{id}/approve` - Approve project

### MRV Reports
- `POST /projects/{id}/monitoring` - Submit MRV report
- `GET /projects/{id}/monitoring` - List MRV reports
- `GET /projects/{id}/monitoring/{mrv_id}` - Get MRV details
- `POST /projects/{id}/monitoring/{mrv_id}/verify` - Verify MRV

### Credits
- `GET /credits` - List carbon credits
- `GET /credits/{id}` - Get credit details
- `POST /credits/transfer` - Transfer credits
- `POST /credits/{id}/retire` - Retire credit

### Utility
- `GET /health` - Health check endpoint

## Authentication

The mockup server uses a simple bearer token authentication. Include any token in the Authorization header:

```bash
curl -H "Authorization: Bearer mock-token" http://localhost:8000/projects
```

## Example Usage

### Create a Project

```bash
curl -X POST "http://localhost:8000/projects" \
  -H "Authorization: Bearer mock-token" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "Feature",
    "ogcr_version": "0.1.0",
    "profile": "pdd",
    "geometry": {
      "type": "Polygon",
      "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
    },
    "properties": {
      "name": "Test Forest Project",
      "project_type": "afforestation",
      "status": "draft",
      "creation_date": "2024-12-07T10:00:00Z",
      "actor_id": "test-developer"
    }
  }'
```

### List Projects

```bash
curl "http://localhost:8000/projects?status=draft&limit=10"
```

## Development

### Project Structure

```
server/
├── app/
│   └── main.py          # Main FastAPI application
├── Dockerfile           # Docker configuration
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

### Adding New Endpoints

1. Define Pydantic models for request/response
2. Add endpoint function with proper type hints
3. Include authentication dependency if needed
4. Add validation and error handling
5. Update this README

## Testing

Run the test suite:

```bash
pytest
```

## License

MIT License - see LICENSE-SOFTWARE file for details.

Copyright (c) 2025 OGCR Consortium

