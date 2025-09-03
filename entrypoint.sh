#!/usr/bin/env bash
set -euo pipefail

echo "Waiting for Neo4j bolt at neo4j:7687 ..."
# simple TCP wait without extra deps
until (echo > /dev/tcp/neo4j/7687) >/dev/null 2>&1; do
  sleep 1
done
echo "Neo4j is up."

# Ensure db folder exists if you're using SQLite for core Django apps
mkdir -p "$(dirname "${SQLITE_PATH:-/app/db/db.sqlite3}")"

# ensure logs dir exists and is writable
LOG_DIR="${DJANGO_LOG_DIR:-/app/logs}"
mkdir -p "$LOG_DIR"
touch "$LOG_DIR/django.log"
chmod 777 "$LOG_DIR/django.log" || true



# --- Correctly configure and check SQLite parent dir ---
# Use the correct, consistent path for the SQLite database.
# This defaults to /data/sqlite/db.sqlite3, which is mapped to the `sqlite_data` volume.
SQLITE_PATH="${SQLITE_PATH:-/data/sqlite/db.sqlite3}"
SQLITE_DIR="$(dirname "$SQLITE_PATH")"

echo "Ensuring SQLite database directory exists at $SQLITE_DIR..."
# Create the directory if it doesn't exist (permissions already set in Dockerfile)
mkdir -p "$SQLITE_DIR"



echo "Running Django migrations..."
python manage.py migrate --noinput

echo "Installing Neomodel labels..."
# Provided by django_neomodel
python manage.py install_labels

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating superadmin user..."
python manage.py create_superadmin --email admin@example.com --password "StrongP@ss!" || echo "Superadmin might already exist"

echo "Starting Django development server..."
exec python manage.py runserver 0.0.0.0:8000
