# Casting Agency API

The Casting Agency API models a company that is responsible for creating movies and managing and assigning actors to those movies. The API endoints require specific authorization for access by three roles: Casting Assistant, Casting Director and Casting Producer.

## Getting Started

### Installing Dependencies

#### Python 3.7

It's good practise to work within a virtual environment whenever using Python. Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM to handle the database.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension to handle cross origin requests from our frontend server.

## Database Setup for local testing

With Postgres running, restore a database using the ca_test.pgsql file provided.
From terminal run the fllowing commands in sequence:

```bash
dropdb ca_test && createdb ca_test
psql ca_test < ca_test.pgsql
python test_app.py
```

## Running the server locally

First ensure you are working using your created virtual environment.

To run the server, execute:

```bash
source setup.sh
```

## Casting Agency API reference

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
- Authentication:

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
  "error": 404,
  "message": "Not Found",
  "success": false
}
```

The API will return these error types when requests fail:

- 400: Bad request
- 404: Resource not found
- 422: Unprocessable
- 401: AuthError with custom messages
- 403: AuthError with custom messages
- 500: Server error

### Endpoint Library

GET /actors and /movies

GET '/actors'

- General:

  - Get the list of actors
  - Returns an object with two keys, categories, a dictionary object of id: category_string key:value pairs, and success, a boolean for the query execution status.
  - Request parameters: None

- Sample: `curl http://127.0.0.1:5000/actors`

```

{
"categories": {
"1": "Science",
"2": "Art",
"3": "Geography",
"4": "History",
"5": "Entertainment",
"6": "Sports"
},
"success": true
}

```
