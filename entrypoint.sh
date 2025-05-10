#!/bin/sh

# Wait for database to be ready
sleep 5

# Make migrations
python core/manage.py makemigrations

# Apply migrations
python core/manage.py migrate

# Start server
python core/manage.py runserver 0.0.0.0:8000
