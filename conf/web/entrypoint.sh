#!/bin/bash

ls -la ./conf

echo "Waiting for DB to startup"
./conf/wait-for-it.sh db:5432

echo "Applying DB Migrations"
python manage.py migrate

echo "Starting App"
python manage.py runserver 0.0.0.0:8000