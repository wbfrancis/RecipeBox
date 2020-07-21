import os
from flask import Flask, request, jsonify, abort, render_template, Response, flash, redirect, url_for
from sqlalchemy import exc
import json
from flask_cors import CORS, cross_origin
from models import db_drop_and_create_all, setup_db, Recipe, RecipeCollection
from auth import AuthError, requires_auth
import ast


database_name = "recipebox"
# TODO: change to your local username
username = 'williamfrancis'

database_path = 'postgres://{}@localhost:5432/recipebox'.format(username)

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app, database_path)
    cors = CORS(app)
    

    # ENDPOINTS FOR RECIPES
    # #####################

    @app.after_request
    def creds(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def index():
        render_template('frontend/index.html') 


    @app.route('/recipes')
    @cross_origin()
    def get_all_recipes():
        try:
            selection = Recipe.query.all()
            recipes = []
            for e in selection:
                recipes.append(e.format())
            return jsonify({
                "success": True,
                "recipes": recipes
            })
        except Exception as e:
            # print (e)
            return not_found(e)


    @app.route('/recipes/<id>')
    @cross_origin()
    def get_recipe(id):
        try:
            selection = Recipe.query.get(id)
            if (selection is None):
                raise Exception('recipe with id ' + id + 'not found')
            return jsonify({
                "success": True,
                "recipes": selection.format()
            })
        except Exception as e:
            return not_found(e)


    @app.route('/recipes', methods=['POST'])
    @cross_origin()
    @requires_auth('post:recipes')
    def post_new_recipe(token):
        try:
            data = ast.literal_eval(request.data.decode("UTF-8"))
            if not ("title" in data and 
            "ingredients" in data and
            "instructions" in data):
                return bad_request(Exception('bad request'))
            new_title = data["title"]
            new_ingredients = [i for i in data["ingredients"].split('\r\n') if i]
            new_instructions = [i for i in data["instructions"].split('\r\n') if i]
            
            new_recipe = Recipe(title=new_title, ingredients=new_ingredients, instructions=new_instructions)
            new_recipe.insert()
            return jsonify({
                "success": True, 
                "recipes": new_recipe.format()
                })
        except Exception as e:
            # print(e)
            return unprocessable(e)

    @app.route('/recipes/<id>', methods=['PATCH'])
    @requires_auth('patch:recipes')
    def update_recipe(token, id):
        recipe = Recipe.query.get(id)
        if recipe is None:
            return not_found(Exception('not found'))

        try:
            data = ast.literal_eval(request.data.decode("UTF-8"))
            for key, val in data.items():
                if key == 'title':
                    recipe.title = val
                if key == 'ingredients':
                    recipe.ingredients = [i for i in val.split('\r\n') if i]
                if key == 'instructions':
                    recipe.instructions = [i for i in val.split('\r\n') if i]
            recipe.update()

            return jsonify({
                "success": True,
                "recipes": [recipe.format()]
            })
        except Exception as e:
            # print(e)
            return unprocessable(e)

    @app.route('/recipes/<id>', methods=['DELETE'])
    @requires_auth('delete:recipes')
    def delete_recipe(token, id):
        recipe = Recipe.query.get(id)
        if recipe is None:
            return not_found(Exception("id doesn't exist"))

        try:
            recipe.delete()
            return jsonify({
                "success": True,
                "deleted": id
            })
        except Exception as e:
            return unprocessable(e)


    # ENDPOINTS FOR RECIPE COLLECTIONS
    # ################################

    @app.route('/recipe-collections')
    @cross_origin()
    def get_all_recipe_collections():
        try:
            selection = RecipeCollection.query.all()
            collections = []
            for e in selection:
                collections.append(e.format())
            return jsonify({
                "success": True,
                "recipe_collections": collections
            })
        except Exception as e:
            # print(e)
            return not_found(e)

    # @app.route('/recipe-collections/<id>')
    # def get_recipe_collection(id):
    #     try:
    #         selection = RecipeCollection.query.get(id)
    #         if (selection is None):
    #             raise Exception('recipe collection with id ' + id + 'not found')
    #         return jsonify({
    #             "success": True,
    #             "recipe_collections": selection.format()
    #         })
    #     except Exception as e:
    #         return not_found(e)

    @app.route('/recipe-collections', methods=['POST'])
    @cross_origin()
    @requires_auth('post:recipe-collections')
    def post_new_recipe_collection(token):
        try:
            
            data = ast.literal_eval(request.data.decode("UTF-8"))
            if not ("title" in data and 
            "description" in data and
            "recipes" in data):
                return bad_request(Exception('bad request'))
            new_title = data["title"]
            new_description = data["description"]
            new_recipes = [i for i in data["recipes"].split(',') if i]
            new_collection = RecipeCollection(title=new_title, description=new_description)
            new_collection.insert()

            for recipe_id in new_recipes:
                recipe = Recipe.query.get(recipe_id)
                recipe.recipe_collection_id = new_collection.id
                recipe.update()

            return jsonify({
                "success": True, 
                "recipe_collections": [new_collection.format()]
                })
        except Exception as e:
            # print(e)
            return unprocessable(e)

    # @app.route('/recipe-collections/<id>', methods=['DELETE'])
    # @requires_auth('delete:recipe-collections')
    # def delete_recipe_collection(token, id):
    #     collection = RecipeCollection.query.get(id)
    #     if collection is None:
    #         return not_found(Exception("id doesn't exist"))

    #     try:
    #         collection.delete()
    #         return jsonify({
    #             "success": True,
    #             "deleted": id
    #         })
    #     except Exception as e:
    #         return unprocessable(e)


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400


    @app.errorhandler(AuthError)
    def auth_error(ex):
        # print(ex)
        return jsonify({
            "success": False,
            "error": ex.status_code,
            "message": ex.error['code']
        }), ex.status_code

    return app

app = create_app()