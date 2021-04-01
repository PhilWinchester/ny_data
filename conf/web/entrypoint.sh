#!/bin/sh

if [ "$DATABASE" = "mysql" ]
then
    echo "Waiting for mysql..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "MYSQL started"
fi

python src/app.py flush --no-input
python src/app.py migrate

exec "$@"