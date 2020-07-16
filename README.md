# RecipeBox

I wanted to make this as a simple, no frills recipe app for my family. Eventually I want to implement group recipe sharing and version editing in order to really make it feel like a family cookbook.

## Setting Things Up

### Setting Up the Virtual Environment

This is assuming you already have Python3.7+ installed

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


## API Documentation