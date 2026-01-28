# API Documentation

## Overview
GitAnalyzer Pro provides a RESTful API for analyzing GitHub repositories and generating comprehensive documentation.

## Base URL
```
http://localhost:8000
```

## Authentication
Most endpoints require a GitHub token to be provided in the request body for accessing repository data.

## Rate Limiting
- Default: 60 requests per minute per IP
- Configurable via `RATE_LIMIT_PER_MINUTE` environment variable

## Endpoints

### Health Check

#### `GET /`
Check API health status

**Response:**
```json
{
  "status": "healthy",
  "version": "v1",
  "timestamp": "2024-01-28T10:30:00Z",
  "services": {
    "github_api": "operational",
    "ai_service": "anthropic",
    "export_service": "operational"
  }
}
```

---

### Analysis Endpoints

#### `POST /api/analyze`
Start a new repository analysis

**Request Body:**
```json
{
  "repository_url": "https://github.com/owner/repo",
  "github_token": "ghp_xxxxxxxxxxxxx",
  "analyzers": ["scope", "architecture"],  // optional
  "ai_provider": "anthropic"               // optional, default: anthropic
}
```

**Response:** `201 Created`
```json
{
  "analysis_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "pending",
  "created_at": "2024-01-28T10:30:00Z",
  "repository_url": "https://github.com/owner/repo"
}
```

**Errors:**
- `400 Bad Request` - Invalid input
- `502 Bad Gateway` - GitHub API error
- `503 Service Unavailable` - AI service error

---

#### `GET /api/analysis/{analysis_id}/status`
Get the status of an ongoing or completed analysis

**Parameters:**
- `analysis_id` (path) - UUID of the analysis

**Response:** `200 OK`
```json
{
  "analysis_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "processing",
  "progress_percentage": 65,
  "current_step": "Running architecture analyzer",
  "started_at": "2024-01-28T10:30:00Z",
  "completed_at": null,
  "error_message": null
}
```

**Status Values:**
- `pending` - Analysis queued
- `processing` - Analysis in progress
- `completed` - Analysis finished successfully
- `failed` - Analysis encountered an error

---

#### `GET /api/analysis/{analysis_id}/results`
Retrieve complete analysis results

**Parameters:**
- `analysis_id` (path) - UUID of the analysis

**Response:** `200 OK`
```json
{
  "analysis_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "repository_url": "https://github.com/owner/repo",
  "analyzed_at": "2024-01-28T10:35:00Z",
  "scope_document": {
    "project_overview": "...",
    "objectives": ["..."],
    "scope_in": ["..."],
    "scope_out": ["..."],
    "assumptions": ["..."],
    "constraints": ["..."],
    "deliverables": ["..."]
  },
  "architecture": {
    "system_architecture": "...",
    "component_diagram": "@startuml\\n...\\n@enduml",
    "technology_stack": {
      "frontend": ["React", "TypeScript"],
      "backend": ["FastAPI", "Python"]
    }
  },
  "reports": {
    "code_quality_score": 85.5,
    "recommendations": ["..."]
  }
}
```

**Errors:**
- `404 Not Found` - Analysis not found or not completed

---

### Export Endpoints

#### `POST /api/export/{analysis_id}/{format}`
Export analysis results in specified format

**Parameters:**
- `analysis_id` (path) - UUID of the analysis
- `format` (path) - Export format: `pdf`, `markdown`, or `json`

**Query Parameters:**
- `include_diagrams` (optional, boolean) - Include diagram images, default: `true`

**Response:** `200 OK`
```json
{
  "download_url": "/api/download/a1b2c3d4/pdf",
  "file_size_bytes": 1048576,
  "format": "pdf",
  "expires_at": "2024-01-29T10:35:00Z"
}
```

---

#### `GET /api/download/{analysis_id}/{format}`
Download exported file

**Parameters:**
- `analysis_id` (path) - UUID of the analysis
- `format` (path) - File format: `pdf`, `markdown`, `md`, or `json`

**Response:** `200 OK`
Returns the file with appropriate Content-Type header

**Errors:**
- `404 Not Found` - Export file not found

---

## Error Responses

All errors follow this format:

```json
{
  "error": "ErrorClassName",
  "message": "Human-readable error message",
  "timestamp": "2024-01-28T10:30:00Z"
}
```

### Common Error Codes
- `400` - Bad Request (validation error)
- `404` - Resource Not Found
- `500` - Internal Server Error
- `502` - Bad Gateway (external service error)
- `503` - Service Unavailable

---

## Example Usage

### Python
```python
import requests

# Start analysis
response = requests.post('http://localhost:8000/api/analyze', json={
    'repository_url': 'https://github.com/owner/repo',
    'github_token': 'ghp_xxxxxxxxxxxxx',
    'ai_provider': 'anthropic'
})
analysis = response.json()
analysis_id = analysis['analysis_id']

# Check status
status_response = requests.get(f'http://localhost:8000/api/analysis/{analysis_id}/status')
status = status_response.json()

# Get results
if status['status'] == 'completed':
    results = requests.get(f'http://localhost:8000/api/analysis/{analysis_id}/results')
    
# Export to PDF
export = requests.post(f'http://localhost:8000/api/export/{analysis_id}/pdf')
download_url = export.json()['download_url']
```

### JavaScript
```javascript
// Start analysis
const response = await fetch('http://localhost:8000/api/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    repository_url: 'https://github.com/owner/repo',
    github_token: 'ghp_xxxxxxxxxxxxx',
    ai_provider: 'anthropic'
  })
});
const analysis = await response.json();

// Poll status
const checkStatus = async () => {
  const statusRes = await fetch(`http://localhost:8000/api/analysis/${analysis.analysis_id}/status`);
  return await statusRes.json();
};

// Get results when completed
const results = await fetch(`http://localhost:8000/api/analysis/${analysis.analysis_id}/results`);
```

---

## Interactive Documentation

Visit the interactive API documentation at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
