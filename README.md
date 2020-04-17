# Casting Agency API

The Casting Agency API models a company that is responsible for creating movies and managing and assigning actors to those movies. The API endoints require specific authorization permissions for access by three roles defined with varying privileges: Casting Assistant, Casting Director and Casting Producer.

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

With Postgres running, restore a database using the ca_test.pgsql file provided and load the environment variables from setup.sh.
From terminal run the fllowing commands in sequence:

```bash
source setup.sh
dropdb ca_test && createdb ca_test
psql ca_test < ca_test.pgsql
python test_app.py
```

## Running the server locally

First ensure you are working using your created virtual environment.

With Postgres running, to load the environment variables from setup.sh, seed the local database and run the server execute:

```bash
source setup.sh
dropdb ca && createdb ca
psql ca < ca_test.pgsql
flask run --reload
```

## Casting Agency API reference

### Getting Started

- Base URL: `https://casting-agency-app.herokuapp.com/`

  Note that this app can also be run locally hosted at the default, http://127.0.0.1:5000/ as indicated above.

- Authentication: an Auth0 api is used for authenticating the 3 roles with RBAC and Permissions in the Access Token as summarized in this table.

| Role              | JWT                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Permissions                                                                                                                                         |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| casting assistant | eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJrUkVRamxGTkRkRVFVRTRRVVk1UWtReVJrWTNOMFF6UVRVNFFVSTBRa1pDUVRjeFJESTNPUSJ9.eyJpc3MiOiJodHRwczovL3AzZnNuZC5hdXRoMC5jb20vIiwic3ViIjoiN0dubzRwdmF0TUVBRnRvZG10RFNrU2w2WFdhbmRNaG5AY2xpZW50cyIsImF1ZCI6ImNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNTg3MTM2MTg4LCJleHAiOjE1ODcyMjI1ODgsImF6cCI6IjdHbm80cHZhdE1FQUZ0b2RtdERTa1NsNlhXYW5kTWhuIiwic2NvcGUiOiJnZXQ6YWN0b3JzIGdldDptb3ZpZXMgZ2V0OmNhc3QiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsImdldDpjYXN0Il19.nOWcu7vqxrYCNFcLhkbMHYeL3mDnOMCs5-r_Jd7dad9Ib-W6m50B26-b58AKVuiwjml7Gv78njY3fiyZ3xTKPhwUsZQqGmEFn03nsIVfDIX0G8F3IGYu-Cw2miBlekFWtoS5GHPJt1raubMMDrqIod-SJyaCAEzFSnE1a0WtY48rRvt1CRLqBN007tPriRwMCEqOrcGUNi6zNH1BuwMEQ1OTgeLuxO-vJ80v81hibdxoOE8JPBj2RLBYhaG2kRF1ILvS_DaVilTygC64ciqeYa0aOYE8j1pYl-33Y6PdtZwe-Ig0LiCgtyeLddUxOR4nICwpPy-yo8V7IkgjrMTONw                                                                                                                                                                                                                                                               | `get:actors`, `get:movies`, `get:cast`                                                                                                              |
| casting director  | eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJrUkVRamxGTkRkRVFVRTRRVVk1UWtReVJrWTNOMFF6UVRVNFFVSTBRa1pDUVRjeFJESTNPUSJ9.eyJpc3MiOiJodHRwczovL3AzZnNuZC5hdXRoMC5jb20vIiwic3ViIjoiN0dubzRwdmF0TUVBRnRvZG10RFNrU2w2WFdhbmRNaG5AY2xpZW50cyIsImF1ZCI6ImNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNTg3MTM2Mjc3LCJleHAiOjE1ODcyMjI2NzcsImF6cCI6IjdHbm80cHZhdE1FQUZ0b2RtdERTa1NsNlhXYW5kTWhuIiwic2NvcGUiOiJnZXQ6YWN0b3JzIGdldDptb3ZpZXMgcG9zdDphY3RvcnMgcGF0Y2g6bW92aWVzIHBhdGNoOmFjdG9ycyBkZWxldGU6YWN0b3JzIGdldDpjYXN0IiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBhdGNoOmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJnZXQ6Y2FzdCJdfQ.hvUZSpnGHI03h-Mpsl37IUO50k67y2SBBMEWRP_Dc21M1KUP8L94rdkZk7fTUdulXOSK9f1p_TbojfTdH9mKiryQac79PW1dtbonKIPs_VyzqHgthys5nzMC4GEkU42HVPTzih0xNagmT05UuVCF1PuClULwoHilE7OnZgoYN_indWFTQN32qjRwhaz5aGIU4kzi5K_wu1oo9n4fi6yUyqnyyBfqgAr6RqOLzArEUfuHps-Ngn5M1PIBZCCFTuLk9xByz3wQWAtsrc7UzvvXbdx4z3BCwF0G-Iy1uj4oONGiRHJay8NRj8CJz0Rl8z95EcLgscPIdMOhnGn1kLzxbg                                                                                                         | `get:actors`, `get:movies`, `get:cast`, `post:actors`, `patch:actors`, `patch:movies`, `delete:actors`                                              |
| casting producer  | eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJrUkVRamxGTkRkRVFVRTRRVVk1UWtReVJrWTNOMFF6UVRVNFFVSTBRa1pDUVRjeFJESTNPUSJ9.eyJpc3MiOiJodHRwczovL3AzZnNuZC5hdXRoMC5jb20vIiwic3ViIjoiN0dubzRwdmF0TUVBRnRvZG10RFNrU2w2WFdhbmRNaG5AY2xpZW50cyIsImF1ZCI6ImNhc3RpbmctYWdlbmN5IiwiaWF0IjoxNTg3MTM1OTI5LCJleHAiOjE1ODcyMjIzMjksImF6cCI6IjdHbm80cHZhdE1FQUZ0b2RtdERTa1NsNlhXYW5kTWhuIiwic2NvcGUiOiJnZXQ6YWN0b3JzIGdldDptb3ZpZXMgcG9zdDphY3RvcnMgcG9zdDptb3ZpZXMgcGF0Y2g6bW92aWVzIHBhdGNoOmFjdG9ycyBkZWxldGU6YWN0b3JzIGRlbGV0ZTptb3ZpZXMgZ2V0OmNhc3QgcG9zdDpjYXN0IiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIiwicGF0Y2g6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6Y2FzdCIsInBvc3Q6Y2FzdCJdfQ.mwwblqopI94djjrL_gzfRb2l5A0QDNk8udJeM8-1HcUXVqFDFtQxV2YPqREOPwUU_jE4s42v4CbRSpEMs6EOvfGQlfd2L6vdsGLDK_VJy5RuYIPr3Q12Hs4R0didA_JdmvIjwC1mfdjiF3UE2HVKts3KigDE_ina7_6ypa-JT2MfwSbsxjuyevIKGtXTLAD2gF2nu0XhMDLn_rXEu3VnA01qvB-ImthviwD-zVDwn4LetWLnlj2FsUG9jt1nkA_cVysYJQyz8006BBrbG9eTvEUeypCwaT10CZBWWoMLarlMPQP6NzuvT0H-TI9CrbYVVorLTbCVkRRfHw7uO_9jOw | `get:actors`, `get:movies`, `get:cast`, `post:actors`, `post:movies`, `patch:actors`, `patch:movies`, `delete:actors`, `delete:movies`, `post:cast` |

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

- 400: Bad request or AuthError specific messages
- 404: Resource not found
- 401: AuthError with specific Auth header and token error messages
- 403: AuthError with specific JWT permission error messages
- 500: Server error

### Endpoint Library

#### GET endpoints

##### GET '/actors'

- Get the list of actors
- Returns an object with key:value pairs for id, name string, age integer, gender string, and success, a boolean for the query execution status.
- Request parameters: None
- Sample: `curl -H "Authorization: {JWT_get:actors}" https://casting-agency-app.herokuapp.com/actors`

```

{
  "actors": [
    {
      "age": 79,
      "gender": "male",
      "id": 1,
      "name": "Al Pacino"
    },
    {
      "age": 55,
      "gender": "male",
      "id": 2,
      "name": "Keanu Reeves"
    },
    {
      "age": 44,
      "gender": "female",
      "id": 3,
      "name": "Charlize Theron"
    }
  ],
  "success": true
}

```

##### GET '/movies'

- Get the list of movies
- Returns an object with key:value pairs for id, title string, release_date string, and success, a boolean for the query execution status.
- Request parameters: None
- Sample: `curl -H "Authorization: {JWT_get:movies}" https://casting-agency-app.herokuapp.com/movies`

```

{
  "movies": [
    {
      "id": 1,
      "release_date": "1997-10-17",
      "title": "The Devil's Advocate"
    },
    {
      "id": 2,
      "release_date": "1999-03-31",
      "title": "The Matrix"
    }
  ],
  "success": true
}

```

##### GET '/cast'

- Get the list of casting pairs between actors and movies
- Returns an object with key:value pairs for id, actor_id, movie_id, and success, a boolean for the query execution status.
- Request parameters: None
- Sample: `curl -H "Authorization: {JWT_get:cast}" https://casting-agency-app.herokuapp.com/cast`

```

{
  "cast": [
    {
      "actor_id": 1,
      "id": 1,
      "movie_id": 1
    },
    {
      "actor_id": 2,
      "id": 2,
      "movie_id": 1
    },
    {
      "actor_id": 3,
      "id": 3,
      "movie_id": 1
    },
    {
      "actor_id": 2,
      "id": 4,
      "movie_id": 2
    }
  ],
  "success": true
}

```

##### GET 'actors/{actor_id}/movies'

- Get the list of movies by actor_id
- Returns an object with key:value pairs for actor_id, actor name, movies list, and success, a boolean for the query execution status.
- Request path parameters: actor id
- Sample: `curl -H "Authorization: {JWT_get:actors}" https://casting-agency-app.herokuapp.com/actors/2/movies`

```

{
  "actor": "Keanu Reeves",
  "actor_id": 2,
  "movies": [
    "The Devil's Advocate",
    "The Matrix"
  ],
  "success": true
}

```

##### GET 'movies/{movie_id}/actors'

- Get the list of actors by movie_id
- Returns an object with key:value pairs for movie_id, movie title, actors list, and success, a boolean for the query execution status.
- Request path parameters: movie id
- Sample: `curl -H "Authorization: {JWT_get:movies}" https://casting-agency-app.herokuapp.com/movies/1/actors`

```

{
  "actors": [
    "Al Pacino",
    "Keanu Reeves",
    "Charlize Theron"
  ],
  "movie": "The Devil's Advocate",
  "movie_id": 1,
  "success": true
}

```

#### POST endpoints

##### POST '/actors'

- Create a new actor
- Returns an object with actor containing key:value pairs for id, name string, age integer, gender string, and success, a boolean for the query execution status.
- Request body parameters: key:value pairs for name, age, gender in json format
- Sample: `curl -X POST -H "Content-Type: application/json" -H "Authorization: {JWT_post:actors}" -d '{"name": "Robert Downey Jr.", "age": 55, "gender": "male" }' https://casting-agency-app.herokuapp.com/actors`

```

{
  "actor": {
    "age": 55,
    "gender": "male",
    "id": 5,
    "name": "Robert Downey Jr."
  },
  "success": true
}

```

##### POST '/movies'

- Create a new movie
- Returns an object with movie containing key:value pairs for id, title string, release_date string, and success, a boolean for the query execution status.
- Request body parameters: key:value pairs for title, release_date in json format
- Sample: `curl -X POST -H "Content-Type: application/json" -H "Authorization: {JWT_post:movies}" -d '{"title": "Sherlock Holmes 3", "release_date": "2021-12-22" }' https://casting-agency-app.herokuapp.com/movies`

```

{
  "movie": {
    "id": 3,
    "release_date": "2021-12-22",
    "title": "Sherlock Holmes 3"
  },
  "success": true
}

```

##### POST '/cast'

- Create a new casting pair
- Returns an object with cast containing key:value pairs for id, actor id, movie id, and success, a boolean for the query execution status.
- Request body parameters: key:value pairs for actor id, movie id in json format
- Sample: `curl -X POST -H "Content-Type: application/json" -H "Authorization: {JWT_post:cast}" -d '{"actor_id": 4, "movie_id": 3}' https://casting-agency-app.herokuapp.com/cast`

```

{
  "cast": {
    "actor_id": 4,
    "id": 5,
    "movie_id": 3
  },
  "success": true
}

```

#### PATCH endpoints

##### PATCH '/actors/{actor_id}'

- Update an actor
- Returns an object with actor containing key:value pairs for id, name string, age integer, gender string, and success, a boolean for the query execution status.
- Request body parameters: key:value pairs for any of name, age, gender to update in json format
- Request path parameters: actor id
- Sample: `curl -X PATCH -H "Content-Type: application/json" -H "Authorization: {JWT_patch:actors}" -d '{"name": "Roberta Downey Jr.", "age": 45, "gender": "female" }' https://casting-agency-app.herokuapp.com/actors/4`

```

{
  "actor": {
    "age": 45,
    "gender": "female",
    "id": 4,
    "name": "Roberta Downey Jr."
  },
  "success": true
}

```

##### PATCH '/movies'

- Update a movie
- Returns an object with movie containing key:value pairs for id, title string, release_date string, and success, a boolean for the query execution status.
- Request body parameters: key:value pairs for any of title, release_date to update in json format
- Request path parameters: movie id
- Sample: `curl -X PATCH -H "Content-Type: application/json" -H "Authorization: {JWT_patch:movies}" -d '{"title": "Sherlock Holmes future", "release_date": "2025-12-22" }' https://casting-agency-app.herokuapp.com/movies/3`

```

{
  "movie": {
    "id": 3,
    "release_date": "2025-12-22",
    "title": "Sherlock Holmes future"
  },
  "success": true
}

```

#### DELETE endpoints

##### DELETE '/actors/{actor_id}'

- Delete an actor
- Returns an object with the deleted id, and success, a boolean for the query execution status.
- Request path parameters: actor id
- Sample: `curl -X DELETE -H "Authorization: {JWT_delete:movies}" https://casting-agency-app.herokuapp.com/actors/4`

```

{
  "deleted_id": 4,
  "success": true
}

```

##### DELETE '/movies/{movie_id}'

- Delete a movie
- Returns an object with the deleted id, and success, a boolean for the query execution status.
- Request path parameters: movie id
- Sample: `curl -X DELETE -H "Authorization: {JWT_delete:movies}" https://casting-agency-app.herokuapp.com/movies/3`

```

{
  "deleted_id": 3,
  "success": true
}

```
