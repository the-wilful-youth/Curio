#!/bin/bash

echo "Stopping Personal AI Content Vault..."
echo "Stopping all services"

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null
then
    echo "docker-compose could not be found"
    exit 1
fi

# Stop all services
docker-compose down

echo "Services stopped!"