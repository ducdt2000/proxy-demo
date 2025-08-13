#!/bin/bash

# This script ensures that the Python-based Docker services are rebuilt
# before starting the entire application stack.

# Exit immediately if a command exits with a non-zero status.
set -e

echo "=> Forcibly rebuilding Python services..."
docker-compose build --no-cache icap-server icap-server2 mock-http-server

echo "=> Starting all services..."
# The '--remove-orphans' flag removes containers for services that are no longer defined in the docker-compose file.
docker-compose up --remove-orphans 