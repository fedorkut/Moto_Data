#!/bin/sh
# entrypoint.sh

set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting FastAPI application using uvicorn..."

# Replace the shell with the uvicorn process
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
