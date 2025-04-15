#!/usr/bin/env bash

if [ "$DOCKER__AUTO_MIGRATE" = "true" ]; then
  if uv run alembic check; then
    echo "Database is up to date."
  else
    echo "Migrating database..."
    uv run alembic upgrade head
  fi
fi


echo "Start gateway service"

# Необходимо для того что бы он запустился с pid 1
# для адекватного завершения всех процессов при выходе
exec uv run uvicorn src.main:create_app --host=$APP_HOST --port=$APP_PORT
