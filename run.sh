#!/usr/bin/env bash

# Fail script on non-zero exit codes
set -e

# Run migrations
PYTHONPATH=. alembic upgrade head

# Start application
python start.py