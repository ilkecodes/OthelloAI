#!/bin/bash
echo "Stopping services..."
docker-compose down
pkill -f uvicorn || true
echo "✓ Stopped"
