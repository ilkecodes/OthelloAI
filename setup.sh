#!/bin/bash

# AI Marketing Platform - Quick Setup Script
set -e

echo "=================================="
echo "AI Marketing Platform Setup"
echo "=================================="
echo ""

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}→ $1${NC}"
}

# Create directory structure
print_info "Creating project structure..."
mkdir -p backend/app/{models,schemas,api,utils}
mkdir -p data reports logs cache content clients

# Create docker-compose.yml
cat > docker-compose.yml << 'DOCKER'
version: '3.8'

services:
  postgres:
    image: postgres:15
    container_name: marketing_db
    environment:
      POSTGRES_DB: marketing_db
      POSTGRES_USER: marketing_user
      POSTGRES_PASSWORD: marketing_password_2024
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    container_name: marketing_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
DOCKER

print_success "docker-compose.yml created"

# Start Docker services
print_info "Starting Docker services..."
docker-compose up -d
sleep 5

print_success "Setup complete!"
echo ""
echo "Next: Add your API keys to backend/.env"
