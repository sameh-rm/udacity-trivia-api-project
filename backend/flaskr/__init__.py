import sys
import datetime
import os
import random
from flask import Flask, request, abort, jsonify, url_for
from flask import json
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_migrate import Migrate
from .models import Quiz, User, setup_db, Question, Category
from werkzeug.security import check_password_hash
# authentication imports
import jwt
from functools import wraps


QUESTIONS_PER_PAGE = 10


def paginate(selection):
    """
        Returns a json formated list
    """
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formated_data = [record.format() for record in selection]

    return formated_data[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    db = setup_db(app)
    migrate = Migrate(app, db)
    app.config["SECRET_KEY"] = "secret"
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers",
            "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods",
            "GET,POST,PUT,PATCH,DELETE,OPTIONS"
        )
        return response

    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get("xx-auth-token")
            if not token:
                return jsonify({"message": "Token is missing", "success": False}), 404
            try:
                jwt.decode(token, app.config["SECRET_KEY"])
            except:
                return jsonify({"message": "Token is invalid or expired", "success": False}), 403
            return f(*args, **kwargs)
        return decorated

    def decode_token(token):
        return jwt.decode(token, app.config["SECRET_KEY"])

    def generate_token(user: User, exp_hours: int = 12):
        return jwt.encode({"user": user.username, "exp": datetime.datetime.utcnow(
        ) + datetime.timedelta(hours=exp_hours)}, app.config["SECRET_KEY"])

    @app.route("/questions", methods=["GET"])
    def get_paginated_questions():
        try:
            selection = Question.ordered_list()
            questions = paginate(Question.ordered_list())
            res = {
                "success": True,
                "questions": questions,
                "total_questions": len(selection),
                "categories": [category.format() for category in Category.ordered_list()],
                "current_category": Category.ordered_list()[0].format(),
            }
            if len(questions) == 0:
                raise IndexError()
        except:
            import sys
            abort(404, "Invalid page number")
        return jsonify(res), 200

    @app.route("/questions/search", methods=["POST"])
    def search_question():
        search_term = request.get_json()["searchTerm"]
        selection = Question.query.filter(
            Question.question.ilike(f"%{search_term}%")).all()
        questions = paginate(selection)
        res = {
            "success": True,
            "questions": questions,
            "total_questions": len(selection),
        }
        return jsonify(res), 200

    @app.route("/questions/<int:question_id>", methods=["GET"])
    def get_question(question_id):
        question = Question.query.get_or_404(question_id)

        return jsonify({
            "success": True,
            "question": question.format(),
            "categories": [category.format() for category in Category.ordered_list()],

        }), 200

    @app.route("/questions", methods=["POST"])
    def create_question():
        try:
            body = request.get_json()
            question = Question(
                question=body["question"],
                answer=body["answer"],
                category=int(body["category"]),
                rating=int(body["rating"]),
                difficulty=int(body["difficulty"])
            )
            question.insert()
        except:
            abort(422, "bad formated request")

        return jsonify({
            "success": True,
            "question": question.format()
        }), 200

    @app.route("/questions/<int:question_id>", methods=["PUT"])
    def update_question(question_id):
        try:
            question = Question.query.get_or_404(question_id)
            body = request.get_json()
            for key in body:
                if key in question.__dict__:
                    setattr(question, key, body[key])
            question.update()
        except:
            abort(404, "question does not exist")

        return jsonify({
            "success": True,
            "question": question.format()
        }), 200

    @app.route('/questions/<int:question_id>', methods=["DELETE"])
    def delete_question(question_id):
        question = Question.query.get_or_404(question_id)
        res = question.format()
        # get the question category_obj
        # get the questions of the category
        # remove question from the questions of the category
        # delete the question
        question.category_obj.questions.remove(question)
        question.delete()

        return jsonify({
            "success": True,
            "question": res,
        }), 200

    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions_by_category(category_id):
        category = Category.query.get_or_404(category_id)
        questions = [
            question.format()
            for question in category.get_questions()
        ]
        res = {
            "success": True,
            "questions": questions,
            "total_questions": len(questions),
            "currentCategory": category.format()
        }
        return jsonify(res), 200

    @app.route("/quizzes", methods=["POST"])
    @token_required
    def get_quizz():
        category_id = request.get_json()["quiz_category"]
        previous_questions = request.get_json()["previous_questions"]
        question = {}
        # check if a category was selected
        if not category_id == 0:
            # load the selected category
            category = Category.query.get_or_404(category_id)
            # load a question from the selected category
            # filter questions to make sure that's a brand new question
            question = category.questions.filter(
                Question.id.notin_(previous_questions)).order_by(func.random()).first()
        else:
            # load questions from Question model cause no category was selected
            question = Question.query.filter(
                Question.id.notin_(previous_questions)).order_by(
                    func.random()).first()

        res = {
            "success": True,
        }
        if question is not None:
            res["question"] = question.format()

        return jsonify(res), 200

    @app.route("/categories", methods=["GET"])
    def get_available_categories():
        categories = [
            category.format()
            for category in Category.ordered_list()
        ]
        return jsonify({
            "success": True,
            "categories": categories,
            "total_categories": len(categories)
        }), 200

    @app.route("/categories/<int:category_id>", methods=["GET"])
    def get_category(category_id):
        category = Category.query.get_or_404(category_id)

        return jsonify({
            "success": True,
            "category": category.format(),
            "categories": [category.format() for category in Category.ordered_list()],
        }), 200

    @app.route("/categories", methods=["POST"])
    @token_required
    def create_category():
        try:
            body = request.get_json()
            category = Category(
                type=body["type"],
                image_link=body["image_link"],
            )
            category.insert()
        except:
            abort(422, "bad formated request")

        return jsonify(
            {
                "success": True,
                "category": category.format()
            }), 200

    @app.route("/categories/<int:category_id>", methods=["PUT"])
    @token_required
    def update_category(category_id):
        try:
            category = Category.query.get_or_404(category_id)
            body = request.get_json()
            # looping throw the body dictionary
            for key in body:
                # check if the category has attribute of category
                if hasattr(category, key):
                    setattr(category, key, body[key])
            category.update()
        except:
            return jsonify({"message": "cannot find this category make sure you passed the correct ID", "success": False}), 404

        return jsonify({
            "success": True,
            "category": category.format()
        }), 200

    @app.route('/categories/<int:category_id>', methods=["DELETE"])
    @token_required
    def delete_category(category_id):
        try:
            category = Category.query.get_or_404(category_id)
            formated_category = category.format()
            category.delete()

            return jsonify({
                "success": True,
                "category": formated_category,
            }), 200
        except:
            abort(404, "cannot find this category make sure you passed the correct ID")

    @app.route("/users/register", methods=["POST"])
    def create_user():
        try:
            body = request.get_json()
            user = User(body["username"], body["password"])
            user.insert()

            token = generate_token(user)

            return jsonify({"token": token.decode("UTF-8"), "username": user.username, "message": "user has been created"}), 200

        except:

            return jsonify({"message": "this username is taken try another one"}), 422

    @app.route("/users/quizzes", methods=["GET"])
    @token_required
    def get_user_quizzes():
        decoded_token = decode_token(request.headers.get("xx-auth-token"))
        user = User.query.filter_by(
            username=decoded_token["user"]).one_or_none()

        if user:
            quizzes = [quiz.format() for quiz in user.quizzes]
            return jsonify({"success": True, "quizzes": quizzes, }), 200
        else:
            return jsonify({"message": "unAuthorized request, make sure you are logged in", }), 403

    @app.route("/users/login", methods=["POST"])
    def login():
        try:
            body = request.get_json()
            username = body["username"]
            password = body["password"]
            if not username or not password:
                return jsonify({"message": "could not verify"})

            user = User.query.filter_by(username=username).one_or_none()

            if not user:
                return jsonify({"message": "Invalid credentials"}), 404

            if check_password_hash(user.password, password):
                # exp = the token life time
                token = generate_token(user)
                return jsonify({"token": token.decode("UTF-8"),
                                "username": username}), 200
        except:
            return jsonify({"message": "username and password required to login"}), 400

        return jsonify({"message": "could not verify, please check your password and try again"}), 422

    @app.route("/users", methods=["GET"])
    @token_required
    def get_logged_user():
        try:
            token = request.headers.get("xx-auth-token")
            token_decoded = decode_token(token)
            if not token:
                return jsonify({"message": "missing Authentication Token or token is expired"}), 404
            if token_decoded["exp"] < datetime.datetime.utcnow().timestamp():
                return jsonify({"message": "Expired Token"}), 400
            user = User.query.filter_by(
                username=token_decoded["user"]).one_or_none()
            if user:
                return jsonify({"message": "verified", "username": user.username, "token": token}), 200
            else:
                return jsonify({"message": "Invalid Token"}), 403
        except:
            print(sys.exc_info())
            return jsonify({"message": "Expired Token"}), 400

    @ app.route("/users/quizzes", methods=["POST"])
    @ token_required
    def save_user_quiz_score():
        try:
            body = request.get_json()
            token = body["token"]
            score = body["score"]
            category = body["category"]
            decoded_token = decode_token(token)
            user = User.query.filter_by(
                username=decoded_token['user']).one_or_none()
            if user:
                quiz = Quiz(user, score, category)
                quiz.insert()
            else:
                return jsonify({"message": "User not found"}), 404
            if not token:
                return jsonify({"message": "could not verify"}), 403
            return jsonify({"message": "verified", "username": decoded_token["user"], "token": token}), 200
        except:
            abort(403, "Missing Authentication Token")

    '''
  @TODO:
  Create error handlers for all expected errors
  '''

    @ app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": error.description,
            "message": "resource not found"
        }), 404

    @ app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": error.description,
            "message": "unprocessable"
        }), 422

    @ app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": error.description,
            "message": "bad request"
        }), 400

    @ app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": error.description,
            "message": "Method Not Allowed"
        }), 405

    @ app.errorhandler(403)
    def method_forbbiden(error):
        return jsonify({
            "success": False,
            "error": error.description,
            "message": "Foribbden Request",
        }), 403

    return app
