#!/bin/bash
# LeadGen Workflow Deployment Script
# Usage: ./deploy.sh [environment]

set -e

# Load environment variables
if [ -f ".env" ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Ensure data directory exists
mkdir -p data

# Build Docker images
docker-compose build

# Start services
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

# Test the intake endpoint
echo "Testing intake endpoint..."
curl -s -X POST http://localhost:8000/api/intake \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Business",
    "location": "Test City",
    "url": "http://test.example.com"
  }' | jq .

# Show logs
echo "Backend logs:"
docker-compose logs -f backend

echo "Frontend logs:"
docker-compose logs -f frontend