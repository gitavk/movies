#!/bin/bash

set -e

# Wait for the database to be ready
until PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U "$POSTGRES_USER" $POSTGRES_DB -c '\q' 2>/dev/null; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

PYTHONPATH="." python src/scripts/init_db.py 
