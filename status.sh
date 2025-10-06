#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "Service Status:"
echo ""

# Docker
if docker ps | grep -q "marketing_db"; then
    echo -e "${GREEN}✓ PostgreSQL running${NC}"
else
    echo -e "${RED}✗ PostgreSQL not running${NC}"
fi

if docker ps | grep -q "marketing_redis"; then
    echo -e "${GREEN}✓ Redis running${NC}"
else
    echo -e "${RED}✗ Redis not running${NC}"
fi

# Backend
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Backend running${NC}"
else
    echo -e "${RED}✗ Backend not running${NC}"
fi
