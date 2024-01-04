# FileSense

FileSense is a Full-Stack project based on multiple technologies such as
Flask and Gunicorn, Nginx, PostgreSql, as well as two well-known AI libraries,
TxtAi and SpaCy.

The project is built on Docker for easier management and deplyment.

## Usage
In order to run the application, make sure docker is installed on your machine.
Navigate in the project's parent directory and run:

```bash
chmod +x ./build-docker.sh && ./build-docker.sh
```

This will open the server on `localhost:8000`.
The configuration can be changed from docker-compose.yaml.

## Backend
For the backend, we used the Flask python framework which is runned by Gunicorn
for better request handling. The Flask application implements two main elements
(blueprints): account management and thecore app. The `accounts` blueprint
takes care of the user register/login functionality, while the `core` blueprint
is responsible for document handling.

Documents can be uploaded and then be searched either by similarity (which uses
TxtAi's embeddings in order to find the best matching documents based on your
input), or by keywords (which uses SpaCy's nlp in order to extract the nouns/
keywords from the query and search them through the database - still in Beta).

On top of flask and gunicorn resides a nginx server, which is responsible
for faster static files delivery.

Each one of the main components is built in its separate Docker container (the
containers are communicating), thus simulating a real-life production
environment.

## Frontend
We used the Bootstrap toolkit to enhance the user interface of our application.
By utilizing Bootstrap's pre-built components, we were able to ensure a
consistent design across different devices and screen sizes. Among the
components used are cards, buttons and a jumbotron.
For the layout and alignments, we used Flexbox.

In the development process, we integrated buttons, a navigation bar and a data
collection box, thus contributing to the functionality of the site and we
focused on creating a pleasant and attractive interface by choosing a suitable
color palette. The styles applied to these elements, as well as the background,
can be found in the style.css file.

## Contribution
* Backend - [Buzdea Matei](https://github.com/MateiBuzdea)
* Frontend - [Similea Alin](https://github.com/AlinS1/),
    [Croitoru Bogdan](https://github.com/bogdan1775)
