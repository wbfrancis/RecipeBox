import os
from flask import Flask, request, jsonify, abort, render_template, Response, flash, redirect, url_for
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Recipe, RecipeCollection
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# db_drop_and_create_all()
# ENDPOINTS FOR RECIPES
# #####################


@app.route('/recipes')
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
        return not_found(e)


@app.route('/recipes/<id>')
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
@requires_auth('post:recipes')
def post_new_recipe(token):
    try:
        data_json = request.get_json()
        if not ("title" in data_json and 
        "ingredients" in data_json and
        "instructions" in data_json):
            bad_request(Exception('bad request'))
        new_title = data_json["title"]
        new_ingredients = data_json["ingredients"]
        new_instructions = data_json["instructions"]
        new_recipe = Recipe(title=new_title, ingredients=new_ingredients, instructions=new_instructions)
        new_recipe.insert()
        return jsonify({
            "success": True, 
            "recipes": [new_recipe.format()]
            })
    except Exception as e:
        return unprocessable(e)

@app.route('/recipes/<id>', methods=['PATCH'])
@requires_auth('patch:recipes')
def update_recipe(token, id):
    recipe = Recipe.query.get(id)
    if recipe is None:
        return not_found(Exception('not found'))

    try:
        body = request.get_json()
        for key, val in body.items():
            print('FILL OUT FILL OUT FILL OUT')
            # if key == 'title':
            #     drink.title = val
            # elif key == 'recipe':
            #     drink.recipe = json.dumps(val)
            # else:
            #     raise Exception(
            #         'You\'re trying to update a value that doesn\'t exist')
        recipe.update()

        return jsonify({
            "success": True,
            "recipes": [recipe.format()]
        })
    except Exception as e:
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
        return not_found(e)

@app.route('/recipe-collections/<id>')
def get_recipe_collection(id):
    try:
        selection = RecipeCollection.query.get(id)
        if (selection is None):
            raise Exception('recipe collection with id ' + id + 'not found')
        return jsonify({
            "success": True,
            "recipe_collections": selection.format()
        })
    except Exception as e:
        return not_found(e)

@app.route('/recipe-collections', methods=['POST'])
@requires_auth('post:recipe-collections')
def post_new_recipe_collection(token):
    pass

@app.route('/recipe-collections/<id>', methods=['PATCH'])
@requires_auth('patch:recipe-collections')
def update_recipe_collection(token, id):
    pass

@app.route('/recipe-collections/<id>', methods=['DELETE'])
@requires_auth('delete:recipe-collections')
def delete_recipe_collection(token, id):
    collection = RecipeCollection.query.get(id)
    if collection is None:
        return not_found(Exception("id doesn't exist"))

    try:
        collection.delete()
        return jsonify({
            "success": True,
            "deleted": id
        })
    except Exception as e:
        return unprocessable(e)




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
    return jsonify({
        "success": False,
        "error": ex.status_code,
        "message": ex.error['code']
    }), ex.status_code
