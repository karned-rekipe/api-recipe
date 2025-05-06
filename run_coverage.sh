#!/bin/bash

# Set environment variables for testing
export PYTHONUNBUFFERED=True
export WORKERS=1
export API_NAME=api-recipe
export API_TAG_NAME=recipes
export URL_API_GATEWAY=http://localhost:8000

# Keycloak Configuration (using placeholder values for testing)
export KEYCLOAK_HOST=http://localhost:8080
export KEYCLOAK_REALM=master
export KEYCLOAK_CLIENT_ID=test-client
export KEYCLOAK_CLIENT_SECRET=test-secret

# Redis Configuration
export REDIS_HOST=localhost
export REDIS_PORT=6379
export REDIS_DB=0
export REDIS_PASSWORD=test-password

# Run pytest with coverage
python -m pytest --cov=. --cov-report=xml --cov-report=term

# Print location of coverage report
echo "Coverage XML report generated at: $(pwd)/coverage.xml"