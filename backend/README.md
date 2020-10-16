# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

- [ ]
- [ ] Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.
- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

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

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

REVIEW_COMMENT

# Endpoints

### Users

```json
POST '/users/register'
- Creates A new user
- Requires username,password
- Returns:{
           "token":"eyJ0eXAiOiJKV1QiLCJhbGciqrasfaxzvzvOiJIUqeqeqezI1NiJ9
                   .eyJ1oxNjAyODI0NTQyfQ.Qx2enXS508gLCs-PBnRhBFTCYVlOWmpax_YC1G4MZWY",
           "username": "username",
           "message": "user has been created"
}

GET '/users/quizzes'
- Fetchs the quizzes of a sepcifec user
- Requires ["xx-auth-token", "Header"]
- Returns:{
  "quizzes": [
    {
      "id": 1,
      "result": 2,
      "category": {
        "id": 1,
        "image_link": null,
        "type": "Science"
      },
      "user": {
        "id": 1,
        "name": "username"
      }
    }
  ],
  "success": true
}
POST '/users/login'
- Requiers A username, password
- Returns:{
           "token": "eyJ0eXAiOiJKV1QiLCJhbGciqrasfaxzvzvOiJIUqeqeqezI1NiJ9
                   .eyJ1oxNjAyODI0NTQyfQ.Qx2enXS508gLCs-PBnRhBFTCYVlOWmpax_YC1G4MZWY",
           "username": "username"
}

POST '/users'
- Requires A jwt-token ["xx-auth-token" Header]
- Returns:{
           "username": "username",
}
```

### Categories

```json
GET '/categories'
- Fetches a list of categories
- Request Arguments: None
- Returns:{
           "success": true ,
           "categories":[
                         {"id":1 , type": "Science", "image_link":"URL"},
                         {"id":2 : "type": "Art", "image_link":"URL"},
                         {"id":3 : "type": "Geography", "image_link":"URL"},
                         {"id":4 : "type": "History", "image_link":"URL"},
                         {"id":5 : "type": "Entertainment", "image_link":"URL"},
                         {"id":6 : "type": "Sports", "image_link":"URL"}
           ]
           "total_categories": 6
}


GET '/categories/<int:category_id>'
- Fetches an object contains a Category
- Request Arguments: category_id
- Returns:{
           "success": true ,
           "category":{"id":1 , "type": "Science", "image_link":"URL"}
}


POST '/categories'
- Creates a new Category
- Requiers ["xx-auth-token" "Header"]
- Request Arguments: None
- Request Body:{
                 "type": "some_type",
                 "image_link": "some_url",
}
- Returns:{
            "success": True,
            "category": {
                           "id":1 ,
                           "type": "Science",
                           "image_link":"URL"
            }
}


PUT '/categories/<int:category_id>'
- Updates an existed Category
- Requiers ["xx-auth-token" "Header"]
- Request Arguments: category_id // 1
- Request Body:{
                 "type": "Development",
                 "image_link": "some_url",
}
- Returns:{
            "success": true,
            "category": {
                           "id":'1' ,
                           "type": "Development",
                           "image_link":"some_url"
            }
}


DETELE '/categories/<int:category_id>'
- Deletes an existed Category
- Requiers ["xx-auth-token" "Header"]
- Request Arguments: category_id // int
- Request Body: No Body
- Returns:{
            "success": true,
            "category": {
                           "id":'1' ,
                           "type": "Science",
                           "image_link":"URL"
            }
}
```

### Questions

```json
GET '/questions'
- Fetches an object contains a list of questions, categories and the current Category
- Request Arguments: None
- Returns:{
  "categories": [
    {
      "id": 1,
      "image_link": "some_url",
      "type": "Science"
    }
  ],
  "current_category": {
    "id": 1,
    "image_link": "some_url",
    "type": "Science"
  },
  "questions": [
    {
      "answer": "Apollo 13",
      "category": {
        "id": 5,
        "image_link": null,
        "type": "Entertainment"
      },
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
      "rating": 4
    },
    {
      "answer": "Tom Cruise",
      "category": {
        "id": 5,
        "image_link": null,
        "type": "Entertainment"
      },
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
      "rating": 3
    },
],
  "success": true,
  "total_questions": 19
}


GET '/categories/<int:category_id>/questions'
- Fetches Questions of the selected category
- Request Arguments: category_id// int
- Returns:{
    "currentCategory": {
        "id": 3,
        "image_link": null,
        "type": "Geography"
    },
    "questions": [
        {
            "answer": "Lake Victoria",
            "category": {
                "id": 3,
                "image_link": null,
                "type": "Geography"
            },
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?",
            "rating": 1
        },
        {
            "answer": "The Palace of Versailles",
            "category": {
                "id": 3,
                "image_link": null,
                "type": "Geography"
            },
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?",
            "rating": 1
        },
        {
            "answer": "Agra",
            "category": {
                "id": 3,
                "image_link": null,
                "type": "Geography"
            },
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?",
            "rating": 1
        }
    ],
    "success": true,
    "total_questions": 3
}


GET '/questions/<int:question_id>'
- Fetches the selected Question
- Request Arguments: question_id// int
- Returns:{
    "question": {
    "answer": "Maya Angelou",
    "category": {
      "id": 4,
      "image_link": "some_url",
      "type": "History"
    },
    "difficulty": 2,
    "id": 5,
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
    "rating": 1
  },
  "success": true
}

POST '/questions'
- Creates a new Question
- Request Arguments: None
- Request Body:{
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
        "answer": "Maya Angelou",
        "difficulty": 4,
        "rating": 3,
        "category":4
    }
- Returns:{
    "question": {
        "answer": "Maya Angelou",
        "category": {
            "id": 4,
            "image_link": null,
            "type": "History"
        },
        "difficulty": 4,
        "id": 24,
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
        "rating": 3
    },
    "success": true
}


PUT '/questions/<int:question_id>'
- Updates an existed Question
- Request Arguments: question_id // 1
- Request Body:{
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
        "answer": "Maya Angelou",
        "difficulty": 2,
        "rating": 1,
        "category":3
    }
- Returns:{
    "question": {
        "answer": "Maya Angelou",
        "category": {
            "id": 3,
            "image_link": null,
            "type": "Geography"
        },
        "difficulty": 2,
        "id": 24,
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
        "rating": 1
    },
    "success": true
}


DETELE '/questions/<int: question_id>'
- Deletes an existed Question
- Request Arguments: category_id // int
- Request Body: No Body
- Returns:{
    "question": {
        "answer": "Maya Angelou",
        "category": {
            "id": 3,
            "image_link": null,
            "type": "Geography"
        },
        "difficulty": 2,
        "id": 24,
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
        "rating": 1
    },
    "success": true
}
```

### Quizzes

```json
POST "/quizzes"
- returns a random question from a specific category or all categories
- requires "xx-auth-token" header
- all categories id = 0
- Request Body:{
        "quiz_category": 2,
        "previous_questions": []
    }
- Returns:{
    "question": {
        "answer": "Escher",
        "category": {
            "id": 2,
            "image_link": null,
            "type": "Art"
        },
        "difficulty": 1,
        "id": 16,
        "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?",
        "rating": 1
    },
    "success": true
}
```

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
