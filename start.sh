#!/bin/bash
# Railway deployment startup script
# Properly handles environment variable expansion

set -e  # Exit on error

# Get port from environment or use default
PORT=${PORT:-8000}
ENV=${ENV:-production}

echo "🚀 Starting CropPulse API"
echo "📌 Port: $PORT"
echo "📌 Environment: $ENV"

# Start the app
exec uvicorn phase2_backend.main:app \
    --host 0.0.0.0 \
    --port $PORT \
    --timeout-keep-alive 65 \
    --access-log
