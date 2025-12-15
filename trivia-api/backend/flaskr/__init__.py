import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}, r"/*": {"origins": "*"}})

    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        formatted_questions = [question.format() for question in selection]
        return formatted_questions[start:end]

    @app.route('/')
    def health():
        return jsonify({'success': True, 'message': 'Trivia API ready'}), 200

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        if not categories:
            abort(404)
        categories_dict = {category.id: category.type for category in categories}
        return jsonify({
            'success': True,
            'categories': categories_dict
        })

    @app.route('/questions')
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        if len(current_questions) == 0:
            abort(404)

        categories = Category.query.order_by(Category.id).all()
        categories_dict = {category.id: category.type for category in categories}

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': categories_dict,
            'current_category': None
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        if question is None:
            abort(404)
        try:
            question.delete()
            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except Exception:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_or_search_question():
        data = request.get_json()
        if data is None:
            abort(400)

        search_term = data.get('searchTerm')
        if search_term is not None:
            selection = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            current_questions = [q.format() for q in selection]
            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection),
                'current_category': None
            })

        question_text = data.get('question')
        answer_text = data.get('answer')
        category = data.get('category')
        difficulty = data.get('difficulty')

        if not question_text or not answer_text or category is None or difficulty is None:
            abort(400)

        try:
            question = Question(
                question=question_text,
                answer=answer_text,
                category=int(category),
                difficulty=int(difficulty)
            )
            question.insert()
            return jsonify({
                'success': True,
                'created': question.id
            }), 201
        except Exception:
            abort(422)

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        category = Category.query.get(category_id)
        if category is None:
            abort(404)
        selection = Question.query.filter(Question.category == category_id).all()
        current_questions = [q.format() for q in selection]
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'current_category': category.type
        })

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        data = request.get_json()
        if data is None:
            abort(400)

        previous_questions = data.get('previous_questions', [])
        quiz_category = data.get('quiz_category')
        if quiz_category is None or 'id' not in quiz_category:
            abort(400)

        category_id = int(quiz_category.get('id'))

        if category_id == 0:
            questions_query = Question.query
        else:
            questions_query = Question.query.filter(Question.category == category_id)

        remaining_questions = questions_query.filter(~Question.id.in_(previous_questions)).all()

        next_question = None
        if remaining_questions:
            next_question = random.choice(remaining_questions).format()

        return jsonify({
            'success': True,
            'question': next_question
        })

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

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

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

    return app
