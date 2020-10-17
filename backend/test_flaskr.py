from datetime import datetime
from flask import app
import jwt
import os
import unittest
import json
from flask.globals import request
from flask_sqlalchemy import SQLAlchemy
import random
import string
from flaskr import create_app
from flaskr.models import setup_db, Question, Category, Quiz, User
import datetime


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            "postgres", "Sameh416",
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        user = User(username="username", password="password")
        token = self.generate_token(user).decode("UTF-8")
        self.headers = {
            "xx-auth-token": token
        }
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def decode_token(self, token):
        return jwt.decode(token, self.app.config["SECRET_KEY"])

    def generate_token(self, user: User, exp_hours: int = 12):
        return jwt.encode({"user": user.username, "exp": datetime.datetime.utcnow(
        ) + datetime.timedelta(hours=exp_hours)}, self.app.config["SECRET_KEY"])

    def tearDown(self):
        """Executed after reach test"""
        # User.query.delete()
        # Quiz.query.delete()
        # Question.query.delete()
        # Category.query.delete()
        # self.db.session.commit()
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_create_user(self):
        random_username = ''.join(random.choice(
            string.ascii_lowercase) for i in range(15))
        res = self.client().post(
            "/users/register",
            json={"username": random_username, "password": "createdUser"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["username"])
        self.assertTrue(data["token"])

    def test_422_create_user(self):
        if User.query.count() == 0:
            self.test_create_user()
        user = User.query.first()
        res = self.client().post(
            "/users/register",
            json={"username": user.username, "password": "testPassword"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(
            data["message"], "this username is taken try another one")

    def test_login(self):
        if User.query.count() == 0:
            self.test_create_user()
        user = User.query.first()
        res = self.client().post(
            "/users/login",
            json={"username": user.username, "password": "createdUser"},)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["token"])
        self.assertTrue(data["username"])

    def test_404_login(self):
        res = self.client().post(
            "/users/login",
            json={"username": "wrongUserName", "password": "LoginUser"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"], "Invalid credentials")

    def test_422_login(self):
        if User.query.count() == 0:
            self.test_create_user()
        user = User.query.first()
        res = self.client().post(
            "/users/login",
            json={"username": user.username, "password": "wrongPassword"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(
            data["message"], "could not verify, please check your password and try again")

    def test_get_logged_user(self):
        client = self.client()
        user = User.query.first()
        token = self.generate_token(user).decode("UTF-8")
        self.headers = {
            "xx-auth-token": token
        }
        res = client.get("/users", headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["token"])
        self.assertTrue(data["username"])

    def test_403_get_logged_user(self):
        client = self.client()
        token = "iJIUzI1NiJ9.eyJ1c2VyIjoiU2xhcmlzR2FtZXNAZ21"
        self.headers = {
            "xx-auth-token": token
        }
        res = client.get("/users", headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
        self.assertTrue(data["current_category"])

    def test_404_get_paginated_questions_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], "Invalid page number")
        self.assertEqual(data['message'], 'resource not found')

    def test_get_available_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_categories"])
        self.assertTrue(data["categories"])

    def test_search_question(self):
        res = self.client().post("/questions/search",
                                 json={"searchTerm": "What"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])

    def test_get_question(self):
        existed_question_id = Question.query.first().id
        res = self.client().get(
            f"/questions/{existed_question_id}")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])
        self.assertTrue(data["categories"])

    def test_404_get_question(self):
        res = self.client().get(
            "/questions/1000")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        # self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    def test_create_question(self):
        res = self.client().post("/questions", json={
            "question": "New Test Question",
            "answer": "Test Answer",
            "difficulty": 3,
            "category": 1,
            "rating": 1,
        })

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    def test_422_create_question(self):
        res = self.client().post("/questions", json={
            "question": "New Test Question",
            "answer": "Test Answer",
            "difficulty": "difficulty",
            "category": "category"
        })

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        # self.assertEqual(data["error"], 422)
        self.assertEqual(data["message"], "unprocessable")

    def test_update_question(self):
        question = Question.query.first()
        client = self.client()
        res = client.put(
            f"/questions/{question.id}",
            json={
                "question": question.question,
                "answer": question.answer,
                "difficulty": question.difficulty,
                'category': 1,
                "rating": 1
            }
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    def test_404_update_question(self):
        res = self.client().put(
            f"/questions/10000",
            json={
                "question": "question.question",
                "answer": "question.answer",
                "difficulty": "question.difficulty",
                'category': "category"
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_question(self):
        target_id = Question.query.order_by(Question.id.desc()).first().id
        res = self.client().delete(
            f"/questions/{target_id}")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    def test_404_delete_question(self):
        res = self.client().delete(
            "/questions/1000")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_questions_by_category(self):
        res = self.client().get(
            f"/categories/1/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["currentCategory"])

    def test_404_get_questions_by_category(self):
        res = self.client().get(
            "/categories/20/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_category(self):
        existed_category_id = Category.query.first().id
        res = self.client().get(
            f"/categories/{existed_category_id}")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["category"])
        self.assertTrue(data["categories"])

    def test_404_get_category(self):
        res = self.client().get(
            "/categories/1000")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        # self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    def test_create_category(self):
        client = self.client()

        res = client.post("/categories", json={
            "type": "New Test category",
            "image_link": "https://images.pexels.com/photos/221164/pexels-photo-221164.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
        }, headers=self.headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["category"])

    def test_422_create_category(self):
        client = self.client()

        res = client.post("/categories", json={
            "type": None,
        }, headers=self.headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        # self.assertEqual(data["error"], 422)
        self.assertEqual(data["message"], "unprocessable")

    def test_update_category(self):
        client = self.client()

        category = Category.query.first()
        res = client.put(
            f"/categories/{category.id}",
            json={
                "type": "New Test category",
                "image_link": "https://images.pexels.com/photos/221164/pexels-photo-221164.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
            }, headers=self.headers
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["category"])

    def test_404_update_category(self):
        client = self.client()
        res = client.put(
            f"/categories/10000",
            json={
                "type": "New Test category"
            },
            headers=self.headers
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_delete_category(self):
        client = self.client()

        target_id = Category.query.order_by(Category.id.desc()).first().id
        res = client.delete(
            f"/categories/{target_id}", headers=self.headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["category"])

    def test_404_delete_category(self):
        res = self.client().delete(
            "/categories/1000")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_get_quizz(self):
        client = self.client()

        res = client.post(
            f"/quizzes",
            json={"quiz_category": 1,
                  "previous_questions": []},
            headers=self.headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    def test_404_get_quizz(self):
        client = self.client()

        res = client.post(
            "/quizzes",
            json={
                "quiz_category": 15,
                "previous_questions": []}, headers=self.headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
