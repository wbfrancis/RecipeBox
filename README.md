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


## API Documentation

GET (/recipes)

GET (/recipes/:id)

POST (/recipes)

PATCH (/recipes)

DELETE (/recipes)

GET (/recipe-collections)

POST (/recipe-collections)