from enum import unique
import os
from sqlalchemy import Column, String, Integer, create_engine
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
import json

from sqlalchemy.orm import backref
from sqlalchemy.sql.schema import ForeignKey

database_name = "trivia"
database_path = "postgres://{}:{}@{}/{}".format(
    'postgres', 'password', 'localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    return db


'''
Question

'''


class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    category = Column(Integer, ForeignKey(
        "categories.id"))
    difficulty = Column(Integer,  default=1)
    rating = Column(Integer,  default=1)

    def __init__(self, question, answer, category, difficulty, rating):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty
        self.rating = rating

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category_obj.format(),
            'difficulty': self.difficulty,
            'rating': self.rating
        }

    @classmethod
    def ordered_list(cls, order_by: str = "id"):
        return cls.query.order_by(order_by).all()


'''
Category

'''


class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    questions = db.relationship("Question", cascade="all,delete-orphan", backref=backref(
        "category_obj", lazy="select", cascade=""), lazy='dynamic')
    image_link = Column(String)

    def __init__(self, type, image_link):
        self.type = type
        self.image_link = image_link

    def format(self):
        return {
            'id': self.id,
            'type': self.type,
            'image_link': self.image_link
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_questions(self):
        return self.questions

    @classmethod
    def ordered_list(cls, order_by="id"):
        return cls.query.order_by(order_by).all()


class Quiz(db.Model):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer)
    result = Column(Integer, default=0)

    def __init__(self, user, result, category):
        self.user_id = user.id
        self.result = result
        self.category_id = category["id"]

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        category = Category.query.filter_by(id=self.category_id).one_or_none()
        if category:
            category = category.format()
        else:
            category = {"id": 0, "type": "all"}
        return {
            'id': self.id,
            'user': self.user.format(),
            'category': category,
            'result': self.result,
        }


class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    quizzes = db.relationship(
        "Quiz", cascade="all,delete-orphan",
        backref=db.backref("user", lazy="select"), lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password, method='sha256')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'username': self.username,
        }

    @classmethod
    def ordered_list(cls, order_by: str = "id"):
        return cls.query.order_by(order_by).all()
