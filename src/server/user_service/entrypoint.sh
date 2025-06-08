#!/bin/sh

echo "⏳ Waiting for PostgreSQL at postgres:5432..."
while ! nc -z postgres 5432; do
  sleep 1
done

echo "✅ PostgreSQL is up. Running app..."
python app.py
