# Health Checks Documentation

This document describes the health check endpoints and monitoring capabilities of the AI Textbook RAG backend.

## Available Health Check Endpoints

### Basic Health Check
- **Endpoint**: `GET /api/v1/health`
- **Purpose**: Comprehensive health check of all system components
- **Response**: Status of all services and configuration

### Readiness Check
- **Endpoint**: `GET /api/v1/ready`
- **Purpose**: Check if the service is ready to accept traffic
- **Response**: Readiness status of all required dependencies

### Liveness Check
- **Endpoint**: `GET /api/v1/live`
- **Purpose**: Check if the service is running
- **Response**: Basic liveness status

### Deep Health Check
- **Endpoint**: `GET /api/v1/deep-health`
- **Purpose**: Test actual functionality of core services
- **Response**: Detailed test results for all core functions

## Health Check Details

### Vector Database Check
- Tests connectivity to Qdrant
- Verifies collection exists and is accessible
- Reports collection statistics

### Embedding Service Check
- Tests embedding model availability
- Verifies encoding functionality
- Reports embedding dimensions

### Configuration Check
- Validates environment variables
- Checks required settings are present
- Reports configuration status

## Monitoring Integration

### For Kubernetes
The health check endpoints are compatible with Kubernetes liveness and readiness probes:

```yaml
livenessProbe:
  httpGet:
    path: /api/v1/live
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /api/v1/ready
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
```

### For Docker Compose
Health checks can be configured in docker-compose.yml:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

## Response Format

### Health Check Response
```json
{
  "status": "healthy",
  "timestamp": "2023-12-10T10:00:00.000000",
  "service": "AI Textbook RAG API",
  "version": "1.0.0",
  "checks": {
    "vector_db": {
      "status": "healthy",
      "info": {
        "name": "textbook_content",
        "vector_size": 384,
        "points_count": 100,
        "indexed_vectors_count": 100
      }
    },
    "embedding_service": {
      "status": "healthy",
      "embedding_length": 384
    },
    "configuration": {
      "status": "configured",
      "debug_mode": false,
      "embedding_model": "all-MiniLM-L6-v2"
    }
  }
}
```

## Alerting and Monitoring

### Health Check Status Codes
- `200 OK`: Service is healthy
- `503 Service Unavailable`: Service is unhealthy

### Metrics to Monitor
- Health check response time
- Service uptime
- Error rates
- Resource utilization

## Troubleshooting

### Common Health Check Failures

1. **Vector Database Unavailable**
   - Check Qdrant URL and credentials
   - Verify network connectivity
   - Ensure Qdrant service is running

2. **Embedding Service Failure**
   - Check embedding model availability
   - Verify sufficient memory resources
   - Check for model loading errors

3. **Configuration Issues**
   - Validate all required environment variables
   - Check for typos in configuration
   - Ensure correct permissions for services