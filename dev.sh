#!/bin/bash
set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if Docker services running
if ! docker ps | grep -q "marketing_db"; then
    echo -e "${YELLOW}Starting Docker services...${NC}"
    docker-compose up -d
    sleep 3
fi

cd backend

# Activate venv
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

# Install requirements if needed
if [ ! -f "venv/installed" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    touch venv/installed
fi

echo -e "${GREEN}✓ Starting backend on http://localhost:8000${NC}"
echo "API docs: http://localhost:8000/docs"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --reload-exclude "venv/*"
