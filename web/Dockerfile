# pull official base image
FROM python:3.11-slim-buster

# envs for python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# copy files
COPY requirements.txt /app/requirements.txt
COPY wait-for-it.sh /wait-for-it.sh
COPY app/* /app/

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN chmod 755 /wait-for-it.sh

ENTRYPOINT ["/wait-for-it.sh", "$SQL_HOST:$SQL_PORT", "--", "python", "manage.py", "init_db"]