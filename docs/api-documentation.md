# OGCR API Documentation

**Version:** 0.1.0  
**Base URL:** `https://api.ogcr.org/v1`  
**Authentication:** OAuth 2.0, API Keys  
**License:** CC-BY 4.0

## Overview

The OGCR API provides comprehensive access to carbon removal project management, monitoring and verification workflows, and carbon credit operations. The API follows RESTful principles with JSON request and response formats, comprehensive error handling, and extensive filtering capabilities.

This documentation covers all available endpoints, authentication methods, data models, and integration patterns. The API is designed for both human users through web interfaces and automated systems through server-to-server integrations.

## Authentication

### OAuth 2.0 Authentication

The API supports OAuth 2.0 authentication for web applications and mobile clients. The following grant types are supported:

- **Authorization Code Grant**: For web applications with server-side components
- **Client Credentials Grant**: For server-to-server integrations
- **Refresh Token Grant**: For maintaining long-term access

#### Authorization Endpoint
```
GET /oauth/authorize
```

**Parameters:**
- `response_type`: Must be "code"
- `client_id`: Your application's client ID
- `redirect_uri`: Registered redirect URI
- `scope`: Requested permissions (space-separated)
- `state`: CSRF protection token

#### Token Endpoint
```
POST /oauth/token
```

**Parameters:**
- `grant_type`: "authorization_code" or "client_credentials"
- `code`: Authorization code (for authorization_code grant)
- `client_id`: Your application's client ID
- `client_secret`: Your application's client secret
- `redirect_uri`: Must match authorization request

#### Scopes

| Scope | Description |
|-------|-------------|
| `projects:read` | Read access to project data |
| `projects:write` | Create and update project data |
| `projects:approve` | Approve projects (restricted to validators) |
| `mrv:read` | Read access to MRV reports |
| `mrv:write` | Create MRV reports |
| `mrv:verify` | Verify MRV reports (restricted to verifiers) |
| `credits:read` | Read access to credit data |
| `credits:transfer` | Transfer credits |
| `credits:retire` | Retire credits |

### API Key Authentication

For server-to-server integrations, API keys provide a simpler authentication method. Include the API key in the `Authorization` header:

```
Authorization: Bearer YOUR_API_KEY
```

API keys are associated with specific organizations and include built-in rate limiting and scope restrictions.

## Rate Limiting

The API implements rate limiting to ensure fair usage and system stability:

| User Type | Rate Limit |
|-----------|------------|
| Standard Users | 100 requests/minute |
| Verified Organizations | 1,000 requests/minute |
| Registry Operators | 10,000 requests/minute |

Rate limit information is included in response headers:
- `X-RateLimit-Limit`: Maximum requests per window
- `X-RateLimit-Remaining`: Remaining requests in current window
- `X-RateLimit-Reset`: Unix timestamp when window resets

## Error Handling

The API uses standard HTTP status codes and provides detailed error responses in JSON format:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The provided data is invalid",
    "details": [
      {
        "field": "properties.methodology.version",
        "message": "Version must be in semantic version format"
      }
    ],
    "timestamp": "2024-12-07T10:30:00Z",
    "request_id": "req_123456789"
  }
}
```

### Common Error Codes

| HTTP Status | Error Code | Description |
|-------------|------------|-------------|
| 400 | `VALIDATION_ERROR` | Request data validation failed |
| 401 | `AUTHENTICATION_REQUIRED` | Valid authentication required |
| 403 | `INSUFFICIENT_PERMISSIONS` | User lacks required permissions |
| 404 | `RESOURCE_NOT_FOUND` | Requested resource does not exist |
| 409 | `CONFLICT` | Resource conflict (e.g., duplicate ID) |
| 429 | `RATE_LIMIT_EXCEEDED` | Too many requests |
| 500 | `INTERNAL_ERROR` | Server error |

## Project Management Endpoints

### Create Project

Creates a new carbon removal project by submitting a Project Design Document (PDD).

```
POST /projects
```

**Request Body:**

For a complete example of a valid Project Design Document, see [examples/valid_pdd.json](../examples/valid_pdd.json).

```json
{
  "type": "Feature",
  "ogcr_version": "0.1.0",
  "profile": "pdd",
  "geometry": {
    "type": "Polygon",
    "coordinates": [
      [[-105.0, 40.0], [-104.0, 40.0], [-104.0, 41.0], [-105.0, 41.0], [-105.0, 40.0]]
    ]
  },
  "properties": {
    "name": "Forest Restoration Project Alpha",
    "description": "Large-scale afforestation project in Colorado",
    "project_type": "afforestation",
    "methodology": {
      "id": "AR-MET-V1.2",
      "version": "1.2"
    },
    "expected_annual_benefit": 15000,
    "baseline_scenario": "Continued agricultural use with minimal carbon storage"
  }
}
```

**Response (201 Created):**
```json
{
  "id": "proj_abc123def456",
  "status": "draft",
  "created_at": "2024-12-07T10:30:00Z",
  "validation_results": {
    "schema_valid": true,
    "geometry_valid": true,
    "methodology_valid": true
  }
}
```

### Get Project

Retrieves detailed information about a specific project.

```
GET /projects/{projectId}
```

**Response (200 OK):**
```json
{
  "type": "Feature",
  "id": "proj_abc123def456",
  "ogcr_version": "0.1.0",
  "profile": "pdd",
  "geometry": {
    "type": "Polygon",
    "coordinates": [
      [[-105.0, 40.0], [-104.0, 40.0], [-104.0, 41.0], [-105.0, 41.0], [-105.0, 40.0]]
    ]
  },
  "properties": {
    "name": "Forest Restoration Project Alpha",
    "status": "approved",
    "creation_date": "2024-12-07T10:30:00Z",
    "last_updated": "2024-12-07T15:45:00Z",
    "project_type": "afforestation",
    "methodology": {
      "id": "AR-MET-V1.2",
      "version": "1.2"
    }
  },
  "ledger_reference": {
    "transaction_id": "0xabcdef1234567890",
    "block_number": 18765432,
    "timestamp": "2024-12-07T15:45:00Z",
    "ledger_id": "ethereum-mainnet"
  }
}
```

### List Projects

Retrieves a paginated list of projects with filtering options.

```
GET /projects
```

**Query Parameters:**
- `status`: Filter by project status (`draft`, `submitted`, `approved`, etc.)
- `project_type`: Filter by project type (`afforestation`, `soil_carbon`, etc.)
- `methodology`: Filter by methodology ID
- `bbox`: Spatial filter (west,south,east,north)
- `limit`: Number of results per page (default: 20, max: 100)
- `offset`: Number of results to skip
- `sort`: Sort field (`created_at`, `name`, `status`)
- `order`: Sort order (`asc`, `desc`)

**Example Request:**
```
GET /projects?status=approved&project_type=afforestation&limit=50&sort=created_at&order=desc
```

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": "proj_abc123def456",
      "name": "Forest Restoration Project Alpha",
      "status": "approved",
      "project_type": "afforestation",
      "created_at": "2024-12-07T10:30:00Z"
    }
  ],
  "pagination": {
    "total": 150,
    "limit": 50,
    "offset": 0,
    "has_more": true
  }
}
```

### Update Project

Updates an existing project. Only allowed for projects in `draft` status.

```
PUT /projects/{projectId}
```

**Request Body:** Complete project object with modifications

**Response (200 OK):** Updated project object

### Submit Project for Approval

Submits a project for validation and approval.

```
POST /projects/{projectId}/submit
```

**Response (200 OK):**
```json
{
  "status": "submitted",
  "blockchain_reference": {
    "transaction_id": "0xabcdef1234567890",
    "block_number": 18765432
  },
  "submitted_at": "2024-12-07T15:45:00Z"
}
```

### Approve Project

Approves a submitted project. Restricted to authorized validators.

```
POST /projects/{projectId}/approve
```

**Request Body:**
```json
{
  "validation_report_hash": "sha256:abcdef1234567890",
  "comments": "Project meets all methodology requirements"
}
```

**Response (200 OK):**
```json
{
  "status": "approved",
  "approved_at": "2024-12-07T16:00:00Z",
  "approved_by": "validator_xyz789"
}
```

## MRV Management Endpoints

### Submit MRV Report

Submits a monitoring, reporting, and verification report for a specific project.

```
POST /projects/{projectId}/monitoring
```

**Request Body:**

For a complete example of a valid MRV document, see [examples/valid_mrv.json](../examples/valid_mrv.json).

```json
{
  "type": "Feature",
  "ogcr_version": "0.1.0",
  "profile": "mrv",
  "geometry": {
    "type": "Polygon",
    "coordinates": [
      [[-105.0, 40.0], [-104.0, 40.0], [-104.0, 41.0], [-105.0, 41.0], [-105.0, 40.0]]
    ]
  },
  "properties": {
    "project_id": "proj_abc123def456",
    "methodology_id": "AR-MET-V1.2",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "methodology_data": {
      "parameters": {
        "tree_density": 1500,
        "avg_growth_rate": 3.2
      },
      "measurement_devices": [
        {
          "type": "lidar",
          "model": "RIEGL VZ-400i",
          "calibration_date": "2024-01-15"
        }
      ],
      "sampling_strategy": "grid-based"
    },
    "net_removal_estimate": {
      "value": 1123.6,
      "unit": "tCO2e",
      "basis": "Annual net aboveground biomass increment"
    }
  }
}
```

**Response (201 Created):**
```json
{
  "id": "mrv_def456ghi789",
  "status": "pending_verification",
  "created_at": "2024-12-07T11:00:00Z",
  "validation_results": {
    "temporal_valid": true,
    "methodology_compliant": true,
    "no_overlaps": true
  }
}
```

### Get MRV Report

Retrieves a specific MRV report.

```
GET /projects/{projectId}/monitoring/{mrvId}
```

**Response (200 OK):** Complete MRV document

### List MRV Reports

Retrieves MRV reports for a specific project.

```
GET /projects/{projectId}/monitoring
```

**Query Parameters:**
- `status`: Filter by verification status
- `reporting_year`: Filter by reporting year
- `verifier`: Filter by verifier organization
- `limit`: Number of results per page
- `offset`: Number of results to skip

### Verify MRV Report

Records verification results for an MRV report. Restricted to authorized verifiers.

```
POST /projects/{projectId}/monitoring/{mrvId}/verify
```

**Request Body:**
```json
{
  "verification_outcome": "approved",
  "verified_removals": 1050.2,
  "verification_report_hash": "sha256:fedcba0987654321",
  "verifier_comments": "All measurements verified through field inspection"
}
```

**Response (200 OK):**
```json
{
  "status": "verified",
  "verified_at": "2024-12-07T14:30:00Z",
  "verified_by": "verifier_abc123",
  "verified_removals": 1050.2
}
```

## Credit Management Endpoints

### List Credits

Retrieves carbon credits with filtering options.

```
GET /credits
```

**Query Parameters:**
- `status`: Filter by credit status (`active`, `retired`)
- `project_id`: Filter by originating project
- `vintage`: Filter by vintage year
- `owner`: Filter by current owner
- `serial_number_range`: Filter by serial number range

**Response (200 OK):**
```json
{
  "data": [
    {
      "token_id": "cru_123456789",
      "project_id": "proj_abc123def456",
      "vintage_year": 2024,
      "carbon_amount": 1.0,
      "status": "active",
      "owner": "0x1234567890abcdef",
      "serial_number": "CRU-2024-001-000001"
    }
  ],
  "pagination": {
    "total": 1050,
    "limit": 20,
    "offset": 0,
    "has_more": true
  }
}
```

### Get Credit Details

Retrieves detailed information about a specific credit.

```
GET /credits/{creditId}
```

**Response (200 OK):**
```json
{
  "token_id": "cru_123456789",
  "project_id": "proj_abc123def456",
  "mrv_hash": "sha256:abcdef1234567890",
  "vintage_year": 2024,
  "carbon_amount": 1.0,
  "status": "active",
  "owner": "0x1234567890abcdef",
  "serial_number": "CRU-2024-001-000001",
  "issuance_date": "2024-12-07T15:00:00Z",
  "blockchain_reference": {
    "transaction_id": "0x9876543210fedcba",
    "block_number": 18765500
  }
}
```

### Transfer Credits

Transfers ownership of carbon credits.

```
POST /credits/transfer
```

**Request Body:**
```json
{
  "credit_ids": ["cru_123456789", "cru_987654321"],
  "recipient": "0xfedcba0987654321",
  "transfer_reason": "Carbon offset purchase"
}
```

**Response (200 OK):**
```json
{
  "transfer_id": "txf_abc123def456",
  "status": "pending",
  "blockchain_transaction": "0x1111222233334444"
}
```

### Retire Credits

Permanently retires carbon credits for offsetting.

```
POST /credits/{creditId}/retire
```

**Request Body:**
```json
{
  "retirement_reason": "Corporate carbon neutrality program",
  "beneficiary": "Acme Corporation",
  "retirement_note": "Offsetting 2024 business travel emissions"
}
```

**Response (200 OK):**
```json
{
  "status": "retired",
  "retired_at": "2024-12-07T16:30:00Z",
  "retirement_certificate": "cert_xyz789abc123"
}
```

## Data Models

### Project Design Document (PDD)

The PDD extends GeoJSON Feature with carbon-specific properties:

```json
{
  "type": "Feature",
  "id": "string",
  "ogcr_version": "string",
  "profile": "pdd",
  "geometry": "GeoJSON Geometry",
  "bbox": "number[]",
  "properties": {
    "name": "string",
    "description": "string",
    "creation_date": "ISO 8601 string",
    "last_updated": "ISO 8601 string",
    "project_type": "string",
    "status": "enum",
    "actor_id": "string"
  },
  "ledger_reference": {
    "transaction_id": "string",
    "block_number": "number",
    "timestamp": "ISO 8601 string",
    "ledger_id": "string"
  },
  "links": "Link[]"
}
```

### MRV Document

The MRV document structure for monitoring reports:

```json
{
  "type": "Feature",
  "id": "string",
  "ogcr_version": "string",
  "profile": "mrv",
  "geometry": "GeoJSON Geometry",
  "properties": {
    "project_id": "string",
    "methodology_id": "string",
    "start_date": "ISO 8601 string",
    "end_date": "ISO 8601 string",
    "methodology_data": "object",
    "net_removal_estimate": {
      "value": "number",
      "unit": "string",
      "basis": "string"
    },
    "verification_status": "enum",
    "verification_date": "ISO 8601 string",
    "verifier_info": "object"
  }
}
```

### Carbon Removal Unit (CRU)

Carbon credit token representation:

```json
{
  "token_id": "string",
  "project_id": "string",
  "mrv_hash": "string",
  "vintage_year": "number",
  "carbon_amount": "number",
  "retired": "boolean",
  "retirement_reason": "string",
  "retirement_timestamp": "ISO 8601 string",
  "retired_by": "string",
  "serial_number": "string",
  "owner": "string"
}
```

## Webhooks

The API supports webhooks for real-time notifications of important events.

### Webhook Events

| Event Type | Description |
|------------|-------------|
| `project.created` | New project created |
| `project.submitted` | Project submitted for approval |
| `project.approved` | Project approved |
| `project.rejected` | Project rejected |
| `mrv.submitted` | MRV report submitted |
| `mrv.verified` | MRV report verified |
| `mrv.rejected` | MRV report rejected |
| `credit.issued` | Credits issued |
| `credit.transferred` | Credits transferred |
| `credit.retired` | Credits retired |

### Webhook Configuration

Configure webhooks through the API:

```
POST /webhooks
```

**Request Body:**
```json
{
  "url": "https://your-app.com/webhooks/carbon-registry",
  "events": ["project.approved", "credit.issued"],
  "secret": "your-webhook-secret"
}
```

### Webhook Payload

Webhook payloads include event metadata and relevant data:

```json
{
  "event": "project.approved",
  "timestamp": "2024-12-07T16:00:00Z",
  "data": {
    "project_id": "proj_abc123def456",
    "status": "approved",
    "approved_by": "validator_xyz789"
  }
}
```

## SDKs and Libraries

Official SDKs are available for popular programming languages:

- **JavaScript/TypeScript**: `@carbon-registry/sdk-js`
- **Python**: `carbon-registry-sdk`
- **Go**: `github.com/carbon-registry/sdk-go`
- **Java**: `com.carbon-registry:sdk-java`

### JavaScript Example

```javascript
import { CarbonRegistryClient } from '@carbon-registry/sdk-js';

const client = new CarbonRegistryClient({
  apiKey: 'your-api-key',
  baseUrl: 'https://api.carbon-registry.org/v1'
});

// Create a new project
const project = await client.projects.create({
  type: 'Feature',
  ogcr_version: '0.1.0',
  profile: 'pdd',
  geometry: {
    type: 'Polygon',
    coordinates: [/* coordinates */]
  },
  properties: {
    name: 'My Carbon Project',
    project_type: 'afforestation'
  }
});

console.log('Project created:', project.id);
```

## Testing and Development

### Sandbox Environment

A sandbox environment is available for testing and development:

- **Base URL**: `https://api-sandbox.carbon-registry.org/v1`
- **Authentication**: Same as production
- **Data**: Test data that can be freely modified
- **Rate Limits**: Relaxed for development

### API Testing Tools

Interactive API documentation and testing tools are available at:
- **Swagger UI**: `https://api.carbon-registry.org/docs`
- **Postman Collection**: Available for download
- **OpenAPI Specification**: `https://api.carbon-registry.org/openapi.json`

This comprehensive API documentation provides all the information needed to integrate with the Carbon Registry system. For additional support, please refer to the developer portal or contact the technical support team.

