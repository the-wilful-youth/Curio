#!/bin/bash

echo "Starting Personal AI Content Vault..."
echo "This will start all services using Docker Compose"

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null
then
    echo "docker-compose could not be found"
    echo "Please install Docker Compose to run this script"
    exit 1
fi

# Start all services
docker-compose up -d

echo "Services started!"
echo ""
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "To stop the services, run: docker-compose down"
echo "To view logs, run: docker-compose logs -f"