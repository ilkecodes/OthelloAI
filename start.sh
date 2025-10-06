#!/bin/bash
set -e

GREEN='\033[0;32m'
NC='\033[0m'

echo "Starting Docker services..."
docker-compose up -d
sleep 3
echo -e "${GREEN}✓ Services started!${NC}"
echo ""
echo "Run: ./dev.sh to start backend"
