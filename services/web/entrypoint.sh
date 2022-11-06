#!/bin/bash

# Verifies that Postgres is up and healthy before init DB
if [ "$DB_ENGINE" = "postgresql" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"

    echo "Deleting existing tables..."
    python manage.py delete_db
    echo "Creating the database tables..."
    python manage.py create_db
    echo "Tables created"

    echo "Creating a Doctor"
    python manage.py add_user nurse 1802961@sit.singaporetech.edu.sg

    echo "Creating a Nurse"
    python manage.py add_user doctor heng.jz98@gmail.com

fi

# if [ "$CMS_DEBUG" = "1" ]
# then
#     echo "Deleting existing tables..."
#     python manage.py delete_db
#     echo "Creating the database tables..."
#     python manage.py create_db
#     echo "Tables created"
# fi

exec "$@"
