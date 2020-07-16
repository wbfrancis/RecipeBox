import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from api import create_app
from database.models import setup_db, Recipe, RecipeCollection


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "recipe_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            'question' : 'why?',
            'answer' : 'cuz',
            'category' : 5,
            'difficulty' : 5
        }

        self.id_to_delete = -1
    
    def tearDown(self):
        """Executed after each test"""
        pass

    
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_all_recipes(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))


    def test_get_recipe(self):
        res = self.client().get('/categories/13')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_not_found(self):
        pass

    def test_post_recipe(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        self.id_to_delete = data['new_question']['id']
        print(self.id_to_delete)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['new_question'])
        self.assertEqual(data['success'], True)

    def test_bad_request(self):
        pass

    def test_patch_recipe(self):
        pass

    def test_unprocessable(self):
        pass

    def test_delete_recipe(self):
        arr = Question.query.all()
        question = arr[len(arr)-1]
        string = f'/questions/{question.id}'
        res = self.client().delete(string)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['deleted_question'])
        self.assertEqual(data['success'], True)

    def test_not_found(self):
        pass

    def test_get_all_recipe_collections(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_post_recipe_collection(self):
        pass

    def test_bad_request(self):
        pass

    def chef_post_recipe(self):

    def unauthorized_delete(self):
        pass

    def post_recipe_collection(self):
        pass

    def delete_recipe(self):
        pass




    def test_404_bad_id(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')



   

    def test_422_no_new_data(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    

    

    def test_404_question_not_found(self):
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_404_invalid_id(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')



    def test_get_quiz_question(self):
        res = self.client().post('/quizzes', json={'previous_questions' : [], 'quiz_category': Category.query.first().format()})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])
        self.assertEqual(data['success'], True)

    def test_400_invalid_category_syntax(self):
        res = self.client().post('/quizzes', json={'previous_questions' : [], 'quiz_category': None})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_404_category_not_found(self):
        res = self.client().post('/quizzes', json={'previous_questions' : [], 'quiz_category': Category('Brainteasers').format()})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()