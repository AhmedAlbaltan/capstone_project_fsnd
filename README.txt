Introduction 

This project is my last project for Udacity's  FSND. 
This project is 

Getting started


This project depends onPython and pip.

Installing project dependencies

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

Running the server

first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
```
Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app` directs flask to use the `app` file to find the application. 


Project deployed at:
https://capstoneappfsnd.herokuapp.com/



This app connects to a Postgres server hosted in Heroku. An account login with specific permissions is needed in order to view, add, update, and remove movies and actors. These are specified below.

Producer login (can view, add, edit, and remove movies and actors):
* email: producer@test.com
* password: Test123!
Casting director login (can view, add and edit only):
* email: casting-director@test.com
* password: Test123!

Casting assistant login (can view actors and movies only):
* email: casting-assistant@test.com
* password: Test123!

OATH login url. JWTs for these appear in the url after successfull login. Those tokens are needed to test the different APIs.
https://udacity-fsnd-lastpro.eu.auth0.com/authorize?audience=CastingAgency&response_type=token&client_id=uOOJ5SPoziP2m96Z5SqN4qPAL5OVOTrF&redirect_uri=https://localhost:8000/


API Endpoints

HTTP Status Codes
200 - OK (The request has succeeded)
400 - Bad Request (The server cannot process the request due to a client error)
401 - Unauthorized (The request requires user authentication)
403 - Forbidden (The server understood the request, but is refusing to fulfill it)
404 - Not Found (The requested resource doesn't exist)

Base URL

https://capstoneappfsnd.herokuapp.com/

Get movies (GET Method)
/movies

Add movie (POST Method)
/movies

Requirements 
body:
{
     'title' : '[the title of the movie]’, 
    ‘release_date’ : ‘[movies release date]'
}
headers:
{
     'Content-Type': 'application/json',
     'Authorization': 'Bearer ' + [TOKEN]
}


Get actors (GET Method)
/actors

Add actor(POST Method)
/actors

Requirements 
body:
{
     'name' : 'the name of the actor’ ,
    ‘age’ : [actor’s age] ,
‘gender’: ‘Male/Female’
}
headers:
{
     'Content-Type': 'application/json',
     'Authorization': 'Bearer ' + [TOKEN]
}

Edit movie (PATCH Method)
/movies/[ID]
Requirements(you can update one or all attributes)
body:
{
     'title' : '[New title]',
     'release_date' : '[new date]'
}
headers:
{
     'Content-Type': 'application/json',
     'Authorization': 'Bearer ' + [TOKEN]
}


Edit actor (PATCH Method)
/actors/[ID]
Requirements(you can update one or all attributes)
body:
{
     'name' : '[New name]',
     'age' : '[new age]',
    ‘gender’:’[new gender]’
}
headers:
{
     'Content-Type': 'application/json',
     'Authorization': 'Bearer ' + [TOKEN]
}

Remove movie(DELETE Method)
/movies/[ID]
Requirements
headers:
{
     'Authorization': 'Bearer ' + [TOKEN]
}

Remove actor(DELETE Method)
/actors/[ID]
Requirements
headers:
{
     'Authorization': 'Bearer ' + [TOKEN]
}







Testing
To run the tests, run
```
dropdb test_casting_agency
createdb test_casting_agency
psql test_casting_agency < test_casting_agency.psql
python test_app.py
```
Omit the dropdb command the first time you run tests

Author

This project was created by Ahmed Albaltan
