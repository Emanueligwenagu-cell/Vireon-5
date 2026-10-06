#!/bin/bash
cd "$(dirname "$0")"
echo "Starting WSU Ibhotwe Food Ordering Platform..."
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000