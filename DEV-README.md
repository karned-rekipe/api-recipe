# Development Setup for api-recipe

This document explains how to set up a development environment for the api-recipe service that connects to the other services in the karned docker-compose setup.

## Prerequisites

- Docker installed on your machine
- The karned docker-compose setup running (except for the api-recipe service)
- The karned-network Docker network created

## Setup Instructions

1. First, start your docker-compose setup:
   ```bash
   docker-compose -f /path/to/docker-compose.yml up -d
   ```

2. Stop the api-recipe service from docker-compose:
   ```bash
   docker-compose -f /path/to/docker-compose.yml stop api-recipe-service
   ```

3. Run the development container using the provided script:
   ```bash
   ./dev-docker-run.sh
   ```

This will:
- Stop any existing development container
- Start a new container with your local code mounted
- Connect to the same network as your other services
- Set up all the necessary environment variables

## Development Workflow

1. Make changes to your code using your IDE
2. The changes will be immediately available in the container
3. The service will automatically restart when you save changes to your files (hot-reload)
4. If you need to restart the entire container for any reason:
   ```bash
   docker restart karned-api-recipe
   ```

## Troubleshooting

If you encounter connection issues between services:
- Ensure all services are on the same network: `docker network inspect karned-network`
- Check logs: `docker logs karned-api-recipe`
- Verify environment variables: `docker exec karned-api-recipe env`

## Stopping Development

When you're done with development:
1. Stop the development container:
   ```bash
   docker stop karned-api-recipe
   ```
2. Restart the original service in docker-compose:
   ```bash
   docker-compose -f /path/to/docker-compose.yml start api-recipe-service
   ```
