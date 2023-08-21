#!/bin/sh
set -e

until cd /app
do
    echo "Wait for server volume..."
done

until alembic upgrade head
do
    echo "Waiting for postgres ready..."
done

python main.py --polling
