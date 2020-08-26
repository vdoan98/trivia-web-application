import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  '''
  @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  '''
  @DONE: Use the after_request decorator to set Access-Control-Allow
  '''

  # CORS Headers
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response


  def paginated_questions(request, selection):
      page = request.args.get('page', 1, type=int)
      start = (page - 1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE

      questions = [question.format() for question in selection]
      current_questions = questions[start:end]

      return current_questions

  def get_categories():
      all_categories = Category.query.order_by(Category.id).all()
      categories = {category.id:category.type for category in all_categories}

      return categories

  '''
  @DONE:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def categories():
      categories = get_categories()
      #print(categories)
      if len(categories) == 0:
          abort(404)
      return jsonify({
        'success': True,
        'categories': categories
      })


  '''
  @DONE:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''

  @app.route('/questions', methods=['GET'])
  def questions():
      selection = Question.query.all()
      current_questions = paginated_questions(request, selection)
      categories = get_categories()
      if len(current_questions) == 0:
          abort(404)

      return jsonify({
        'success': True,
        'questions': current_questions,
        'categories': categories,
        'current_category': None,
        'total_questions': len(selection)
      })

  '''
  @DONE:
  Create an endpoint to DELETE question using a question ID.
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
          abort(404)

      question.delete()
      selection = Question.query.all()
      current_questions = paginated_questions(request, selection)

      return jsonify({
        'success': True,
        'deleted': question_id,
        'questions': current_questions,
        'total_questions': len(selection)
      })

  '''
  @DONE:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.
  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''

  @app.route('/questions/add', methods=['POST'])
  def add_question():
      data = request.get_json()
      #data = json.loads(request.data.decode('utf-8'))
      #print(data)
      new_question = data.get('question', '')
      new_answer = data.get('answer', '')
      new_difficulty = data.get('difficulty', '')
      new_category = data.get('category', '')

      if ((new_question == '') or (new_answer == '') or (new_difficulty == '') or (new_category == '')):
          abort(422)
      try:
          question = Question(question=new_question,answer=new_answer,category=new_category,difficulty=new_difficulty)
          #Question.insert(question)
          #print(question['answer'])
          Question.insert(question)
          current_questions =paginated_questions(request, Question.query.all())
          return jsonify({
            'success': True,
            'created':question.id,
            'question': current_questions,
            'total_questions': len(Question.query.all())
          })
      except Exception:
          abort(422)

  '''
  @DONE:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.
  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''

  @app.route('/questions/search', methods=['POST'])
  def search_question():
      form = request.get_json()
      search_term = form.get('searchTerm', '')
      questions = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()
      #print(questions)

      current_questions = paginated_questions(request, questions)
      if len(questions) == 0:
          abort(404)


      return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(Question.query.all()),
        'current_category': [(question['category']) for question in current_questions]
      })

  '''
  @DONE:
  Create a GET endpoint to get questions based on category.
  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''

  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_question_category(category_id):
      selection = Question.query.filter(Question.category == category_id).all()


      current_questions = paginated_questions(request, selection)
      if len(selection) == 0:
          abort(404)


      return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(selection),
        'current_category': category_id
      })

  '''
  @DONE:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.
  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''

  @app.route('/quizzes', methods=['POST'])
  def quizzes():
      data = request.get_json()

      previous_questions = data.get('previous_questions', None)

      quiz_category = data.get('quiz_category', None)

      try:
          if (quiz_category['id'] == 0):
              questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
          else:
              questions = Question.query.filter(Question.category == quiz_category['id'])\
                    .filter(Question.id.notin_(previous_questions)).all()

          if (len(questions) > 0):
              question = random.choice(questions).format()
              return jsonify ({
                'success': True,
                'question': question
              })
          else:
              return jsonify ({
                'success': True,
                'question': None
              })

      except:
          abort(422)

  '''
  Add new category
  '''
  @app.route('/categories/add', methods=['POST'])
  def add_category():
      data = request.get_json()
      #data = json.loads(request.data.decode('utf-8'))
      #print(data)
      new_type = data.get('type', None)
      print(new_type)
      if (new_type == None):
          abort(422)

      try:
          new_category = Category(type=new_type)

          Category.insert(new_category)
          print("Inserted!")

          return jsonify({
            'success': True,
            'created': new_category.id
          })
      except Exception as e:
          print(e)
          abort(405)



  '''
  @DONE:
  Create error handlers for all expected errors
  including 404 and 422.
  '''

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable'
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
      }), 400

  @app.errorhandler(405)
  def not_allow(error):
      return jsonify({
        'success': False,
        'error': 405,
        'message': 'method not allowed'
      }), 405

  @app.errorhandler(500)
  def server_error(error):
      return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal server error'
      })

  return app
