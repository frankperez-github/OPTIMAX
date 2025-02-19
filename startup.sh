#!/bin/bash
# startup.sh
# This script initializes the optimax Docker container with the current local project directory mounted as /app.

# Check if the Docker image 'optimax' exists
if ! docker image inspect optimax >/dev/null 2>&1; then
  echo "Docker image 'optimax' not found. Please build it first with:"
  echo "  docker build -t optimax ."
  exit 1
fi

# Run the optimax container with the local project directory mounted to /app
docker run --rm -it \
  -v "$(pwd)":/app \
  --name optimax \
  optimax
