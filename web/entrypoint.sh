#!/bin/bash

# make static folder rx
chmod a+x -R /app/app/static

/wait-for-it.sh db:5432 -- python3 manage.py create_db
gunicorn -b 0.0.0.0:5000 manage:app
# /wait-for-it.sh db:5432 -- gunicorn -b 0.0.0.0:5000 manage:app