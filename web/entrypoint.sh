#!/bin/bash

/wait-for-it.sh db:5432 -- python3 manage.py create_db
gunicorn -b 0.0.0.0:5000 manage:app