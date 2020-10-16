import os
import unittest
import json
from flask.globals import request
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from flaskr.models import setup_db, Question, Category


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

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

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
        res = self.client().put(
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
        res = self.client().post("/categories", json={
            "type": "New Test category",
            "image_link": "https://images.pexels.com/photos/221164/pexels-photo-221164.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
        })

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["category"])

    def test_422_create_category(self):
        res = self.client().post("/categories", json={
            "type": None,
        })

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        # self.assertEqual(data["error"], 422)
        self.assertEqual(data["message"], "unprocessable")

    def test_update_category(self):
        category = Category.query.first()
        res = self.client().put(
            f"/categories/{category.id}",
            json={
                "type": "New Test category",
                "image_link": "https://images.pexels.com/photos/221164/pexels-photo-221164.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
            }
        )

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["category"])

    def test_404_update_category(self):
        res = self.client().put(
            f"/categories/10000",
            json={
                "type": "New Test category",
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_category(self):
        target_id = Category.query.order_by(Category.id.desc()).first().id
        res = self.client().delete(
            f"/categories/{target_id}")
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
        self.assertEqual(data["message"], "resource not found")

    def test_get_quizz(self):
        res = self.client().post(
            f"/quizzes", json={"quiz_category": 1, "previous_questions": []})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    def test_404_get_quizz(self):
        res = self.client().post(
            "/quizzes", json={"quiz_category": 15, "previous_questions": []})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
