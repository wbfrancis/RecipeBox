import os
import unittest
from dotenv import load_dotenv
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Recipe, RecipeCollection


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "recipe_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        load_dotenv()
        self.admin = os.getenv('ADMIN_TOKEN')
        self.chef = os.getenv('CHEF_TOKEN')

        self.new_recipe = {
            'title': 'Burnt Fish',
            'ingredients': 'Fish\r\nFire',
            'instructions': 'Light Fire\r\nCook fish until it burns',
        }

        self.new_collection = {
            'title': 'Burnt Food',
            'description': "This food is burnt",
            'recipes': '1',
        }

        self.bad_collection = {
            'titel': 'Burnt Food',
            'description': "This food is burnt",
            'recipes': '1',
        }

        self.bad_recipe = {
            'titel': 'Burnt Fish',
            'ingredients': 'Fish\r\nFire',
            'instructions': 'Light Fire\r\nCook fish until it burns',
        }

        self.patch_data = {
            'title': 'Extra Crispy Carp'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after each test"""
        pass

    
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_post_recipe(self):
        res = self.client().post('/recipes', json=self.new_recipe, headers=[
                ('Content-Type', 'text/plain'),
                ('Authorization', f'Bearer {self.admin}')
            ])
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['recipes'])
        self.assertEqual(data['success'], True)


    def test_bad_request(self):
        res = self.client().post('/recipes', json=self.bad_recipe, headers=[
                ('Content-Type', 'text/plain'),
                ('Authorization', f'Bearer {self.admin}')
            ])
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)


    def test_patch_recipe(self):
        self.client().post('/recipes', json=self.new_recipe, headers=[
                ('Content-Type', 'text/plain'),
                ('Authorization', f'Bearer {self.admin}')
            ])

        arr = Recipe.query.all()
        recipe = arr[len(arr)-1]
        string = f'/recipes/{recipe.id}'
        res = self.client().patch(string, json=self.patch_data, headers=[
                ('Content-Type', 'text/plain'),
                ('Authorization', f'Bearer {self.admin}')
            ])
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['recipes'])
        self.assertEqual(data['success'], True)


    def test_unprocessable(self):
        self.client().post('/recipes', json=self.new_recipe, headers=[
                ('Content-Type', 'text/plain'),
                ('Authorization', f'Bearer {self.admin}')
            ])

        arr = Recipe.query.all()
        recipe = arr[len(arr)-1]
        string = f'/recipes/{recipe.id}'
        res = self.client().patch(string, json='heyyy', headers=[
                ('Content-Type', 'text/plain'),
                ('Authorization', f'Bearer {self.admin}')
            ])
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
    

    def test_get_all_recipes(self):
        self.client().post('/recipes', json=self.new_recipe, headers=[
                ('Content-Type', 'text/plain'),
                ('Authorization', f'Bearer {self.admin}')
            ])

        res = self.client().get('/recipes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['recipes']))


    def test_get_recipe(self):
        res = self.client().post('/recipes', json=self.new_recipe, headers=[
                ('Content-Type', 'text/plain'),
                ('Authorization', f'Bearer {self.admin}')
            ])
        data = json.loads(res.data)

        res = self.client().get('/recipes/'+str(data['recipes']['id']))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['recipes']))

    
    def test_delete_recipe(self):
        res = self.client().post('/recipes', json=self.new_recipe, headers=[
                ('Content-Type', 'text/plain'),
                ('Authorization', f'Bearer {self.admin}')
            ])
            
        arr = Recipe.query.all()
        recipe = arr[len(arr)-1]
        string = f'/recipes/{recipe.id}'
        res = self.client().delete(string, headers=[
                ('Content-Type', 'text/plain'),
                ('Authorization', f'Bearer {self.admin}')
            ])
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['deleted'])
        self.assertEqual(data['success'], True)


    def test_not_found(self):
        string = '/recipes/1'
        res = self.client().delete(string, headers=[
                ('Content-Type', 'text/plain'),
                ('Authorization', f'Bearer {self.admin}')
            ])
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


    def test_post_recipe_collection(self):
        self.client().post('/recipes', json=self.new_recipe, headers=[
                ('Content-Type', 'text/plain'),
                ('Authorization', f'Bearer {self.admin}')
            ])

        res = self.client().post('/recipe-collections', json=self.new_collection, headers=[
                ('Content-Type', 'text/plain'),
                ('Authorization', f'Bearer {self.admin}')
            ])
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['recipe_collections'])
        self.assertEqual(data['success'], True)


    def test_bad_request(self):
        self.client().post('/recipes', json=self.new_recipe, headers=[
                ('Content-Type', 'text/plain'),
                ('Authorization', f'Bearer {self.admin}')
            ])

        res = self.client().post('/recipe-collections', json=self.bad_collection, headers=[
                ('Content-Type', 'text/plain'),
                ('Authorization', f'Bearer {self.admin}')
            ])
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)


    def test_get_all_recipe_collections(self):
        self.client().post('/recipes', json=self.new_recipe, headers=[
                ('Content-Type', 'text/plain'),
                ('Authorization', f'Bearer {self.admin}')
            ])

        self.client().post('/recipe-collections', json=self.new_collection, headers=[
                ('Content-Type', 'text/plain'),
                ('Authorization', f'Bearer {self.admin}')
            ])

        res = self.client().get('/recipe-collections')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['recipe_collections']))



    def test_chef_post_recipe(self):
        res = self.client().post('/recipes', json=self.new_recipe, headers=[
                ('Content-Type', 'text/plain'),
                ('Authorization', f'Bearer {self.chef}')
            ])
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['recipes'])
        self.assertEqual(data['success'], True)


    def test_chef_unauthorized_delete(self):
        res = self.client().post('/recipes', json=self.new_recipe, headers=[
                ('Content-Type', 'text/plain'),
                ('Authorization', f'Bearer {self.chef}')
            ])
            
        arr = Recipe.query.all()
        recipe = arr[len(arr)-1]
        string = f'/recipes/{recipe.id}'
        res = self.client().delete(string, headers=[
                ('Content-Type', 'text/plain'),
                ('Authorization', f'Bearer {self.chef}')
            ])
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_admin_post_recipe_collection(self):
        self.client().post('/recipes', json=self.new_recipe, headers=[
                ('Content-Type', 'text/plain'),
                ('Authorization', f'Bearer {self.admin}')
            ])

        res = self.client().post('/recipe-collections', json=self.new_collection, headers=[
                ('Content-Type', 'text/plain'),
                ('Authorization', f'Bearer {self.admin}')
            ])
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['recipe_collections'])
        self.assertEqual(data['success'], True)

    def test_admin_delete_recipe(self):
        res = self.client().post('/recipes', json=self.new_recipe, headers=[
                ('Content-Type', 'text/plain'),
                ('Authorization', f'Bearer {self.admin}')
            ])
            
        arr = Recipe.query.all()
        recipe = arr[len(arr)-1]
        string = f'/recipes/{recipe.id}'
        res = self.client().delete(string, headers=[
                ('Content-Type', 'text/plain'),
                ('Authorization', f'Bearer {self.admin}')
            ])
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['deleted'])
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()