#!/bin/bash
docker-compose down --volumes
docker-compose rm -s -f
docker-compose up --build -d
