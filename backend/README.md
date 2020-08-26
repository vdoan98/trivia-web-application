# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```
`psql -d trivia -U postgres -a -f trivia.psql`

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers. [DONE]
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. [DONE]
3. Create an endpoint to handle GET requests for all available categories. [DONE]
4. Create an endpoint to DELETE question using a question ID. [DONE]
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category. [DONE]
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. [DONE]
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. [DONE]
9. Create error handlers for all expected errors including 400, 404, 422 and 500. [DONE]


## API documentation

### Endpoints
```
GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}


GET '/questions'
- Fetches a list of questions, with limit of 10 question per each API call corresponding to 10 questions per page limit.
- Request Arguments: None
- Returns: A list of objects with 5 keys: id, question, answer, category and difficulty with the corresponding value from database.
- Question object:
{
  'id': 5,
  'question': 'Whose autobiography is entitled 'I Know Why the Caged Bird Sings?'',
  'answer': 'Maya Angelou',
  'category': 4,
  'difficulty': 2
}
{
  'success': True,
  'questions': [...],
  'categories': {'1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"},
   'current_category': None,
   'total_questions': 18
}

DELETE '/questions/<int:question_id>'
- Delete question from database.
- Request Arguments: question id
- Returns: id of the deleted question and a list of the questions remained on the database, in group of 10, as questions. total_questions in the count of all questions existing in the database after the deletion
{
  'success': True,
  'deleted': 5,
  'questions': [...],
  'total_questions': 17
}

POST '/questions/add'
- Add new question from filled form. Database table have type constraints. Incorrect type from form throws error.
- Request Arguments: None
- Returns: id of created question and a list of the questions in the updated database, in group of 10, as questions. total_questions is the count of all existing questions in the database.  
- Question constraints:
  - id: integer
  - question: text
  - answer: text
  - difficulty: integer
  - category: integer
{
  'success': True,
  'created': 13,
  'questions': [...],
  'total_questions': 19
}

POST '/questions/search'
- Search for question based on search term
- Request Arguments: None
- Returns: list of questions with search term. total_question is the count of all question existing in the database.
{
  'success': True,
  'questions': [
  {
    'id': 2,
    'question': 'What movie earned Tom Hanks his third straight Oscar nomination, in 1996',
    'answer': 'Apollo 13',
    'category: 5',
    'difficulty': 1
  }
  ],
  'total_questions': 18,
  'current_category': [5]
}

GET '/categories/<int:category_id>/questions'
- Fetches a list of questions based on category. Question is displayed in group of 10 per page.
- Request Arguments: category id
- Returns: list of questions based on category in group of 10. total_question is the count of all questions existing in the database.
{
  'success': True,
  'questions': [
  {
    'id': 5,
    'question': 'Whose autobiography is entitled 'I Know Why the Caged Bird Sings?'',
    'answer': 'Maya Angelou',
    'category': 4,
    'difficulty': 2
  },
  {
    'id': 2,
    'question': 'What movie earned Tom Hanks his third straight Oscar nomination, in 1996',
    'answer': 'Apollo 13',
    'category: 5',
    'difficulty': 1
  }
  ],
  'total_questions': 2,
  'current_category': 4
}

POST '/quizzes'
- Fetch new question for quiz based on category and previous question seen. Method search for question in database that does not exist in the previous_questions list.
- Request Arguments: None
- Return: question that does not exists in previous_questions and is under the category chosen. If none exist, return None.
{
  'success': True,
  'question': {
    'id': 2,
    'question': 'What movie earned Tom Hanks his third straight Oscar nomination, in 1996',
    'answer': 'Apollo 13',
    'category: 5',
    'difficulty': 1
  }
}

POST '/categories/add'
- Add new category to database. Category type is filled using the form on Add page. Table will automatically assign id to new category.
- Request Arguments: None
- Return: id of new category
{
  'success': True
  'created': 8
}
```
## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql -d trivia -U postgres -a -f trivia.psql
python test_flaskr.py
```
