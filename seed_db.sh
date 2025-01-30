#!/bin/bash

# Script to apply migrations to the DB - create the initial model and seed with the test data

# VIRTUAL_ENV variable will be set only if the script is running in the virtual environment
# If it is not activated, activate it
if [ -z "$VIRTUAL_ENV" ]; then
    source "./venv/bin/activate"
fi

# Remove the db, so we start fresh
rm -f ./PISSDjango/db.sqlite3
# Apply migrations
python3 ./PISSDjango/manage.py migrate
# Seed the db with example data
cat "./PISSDjango/db_test.sql" | python3 ./PISSDjango/manage.py dbshell 