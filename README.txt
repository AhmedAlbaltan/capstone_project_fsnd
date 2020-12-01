Full Stack Capstone Project
This project is the last project in Udacity-FSND where users can answer some trivia questions. The task for this project was to create an API that can achive the following functionality:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

Getting started


This project depends on Nodejs and Node Package Manager (NPM).Python and pip.

Installing project dependencies

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
```
Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app` directs flask to use the `app` file to find the application. 



https://git.heroku.com/capstoneappfsnd.git
postgresql-tapered-77881

casting-assistant@test.com

casting-director@test.com


producer@test.com

https://udacity-fsnd-lastpro.eu.auth0.com/authorize?audience=CastingAgency&response_type=token&client_id=uOOJ5SPoziP2m96Z5SqN4qPAL5OVOTrF&redirect_uri=https://localhost:8000/








Testing
To run the tests, run
```
dropdb test_casting_agency
createdb test_casting_agency
psql test_casting_agency < test_casting_agency.psql
python test_app.py
```
Omit the dropdb command the first time you run tests

