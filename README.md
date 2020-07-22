# RecipeBox

I wanted to make this as a simple, no frills cooking recipe app for my family. Eventually I want to implement group recipe sharing and version editing in order to really make it feel like a family cookbook.

## Setting Things Up

This is assuming you already have Python 3.7+ installed

### The Virtual Environment

First, navigate to src, then in the terminal:

FOR MAC/LINUX:
$ python3 -m venv env

FOR WINDOWS:
$ py -m venv env


Activate the virtual environment:

$ source env/bin/activate


Then to install packages, run:

$ pip3 install -r requirements.txt


### Running the Flask App

There's already a .flaskenv file so all you need to do is run this from the src directory:

$ flask run

And it should start up in development mode.


### Running the Frontend

As long as you have some sort of Live Server functionality (such as is found in VSCode or etc) you should just need to throw up any of the htmls within the frontend directory.


## RBAC and Login Info

Currently there are two users with different roles

Chef (can post and edit recipes)

    email: g@me.com

    password: !mn0ttheb0ss


Admin (can post, edit, delete recipes, can post recipe collections)

    email: l@boss.org

    password: !mtheb0ss


## Models

There are two models for this app. The first is Recipe, which contains a title, an array of ingredients, and an array of instructions, as well as a foreign key if the recipe belongs to a Recipe Collection. The next, Recipe Collection, contains a title, a description, and an array of recipes that are associated with it.

To set up your own database you will need to change the database info in src/database/models.py

## API Documentation

GET (/recipes)
- Fetches a list of all recipes
- Request Arguments: None
- Returns: 

{
    success: True,
    recipes: []
}


GET (/recipes?id=XXX)
- Fetches a recipes
- Request Arguments: the given recipe id
- Returns: list with a single element

{
    success: True,
    recipes: {
            'id': self.id,
            'title': self.title,
            'ingredients': self.ingredients,
            'instructions': self.instructions,
            'recipe_collection_id': self.recipe_collection_id
        }
}

POST (/recipes)
- Posts a new recipe
- Request Arguments: json text/data object in this format
{
    title: X,
    ingredients: X,
    instructions: X,
}       

- Returns: the new recipe

{
    success: True,
    recipes: {
            'id': self.id,
            'title': self.title,
            'ingredients': self.ingredients,
            'instructions': self.instructions,
            'recipe_collection_id': self.recipe_collection_id
        }
}

PATCH (/recipes)
- Edits a recipe
- Request Arguments: json text/data object in this format
{
    title: (if any),
    ingredients: (if any),
    instructions: (if any),
}       

- Returns: the edited recipe

{
    success: True,
    recipes: {
            'id': self.id,
            'title': self.title,
            'ingredients': self.ingredients,
            'instructions': self.instructions,
            'recipe_collection_id': self.recipe_collection_id
        }
}

DELETE (/recipes?id=XXX)
- Deletes a recipe
- Request Arguments: id, see above
- Returns: the deleted recipe

{
    success: True,
    recipes: {
            'id': self.id,
            'title': self.title,
            'ingredients': self.ingredients,
            'instructions': self.instructions,
            'recipe_collection_id': self.recipe_collection_id
        }
}


GET (/recipe-collections)
- Gets all recipe collections
- Request Arguments: id, see above
- Returns: the deleted recipe

{
    success: True,
    recipe_collections: {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'recipes': [
                {
                'id': self.id,
                'title': self.title,
                'ingredients': self.ingredients,
                'instructions': self.instructions,
                'recipe_collection_id': self.recipe_collection_id
                },  
            etc
            ],
    }

}

POST (/recipe-collections)
_ *Not navigable to on the frontend. Found at /new-collection.html*
- Posts a new recipe collection
- Request Arguments: json text/data object in this format
{
    title: X,
    description: X,
    recipes: '14,12,13',
}       

- Returns: the new recipe collection

{
    success: True,
    recipes_collections: XXX
}