import os
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects import postgresql
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json


database_name = "recipebox"
database_path = 'postgres://williamfrancis@localhost:5432/recipebox'
# database_path = "postgres://{}/{}".format('localhost:5432', database_name)
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)

'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

'''
RECIPE
a persistent recipe entity, extends the base SQLAlchemy Model
'''
class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True)
    # title of recipe
    title = Column(String((300)), unique=True)

    # array of strings where each element is a new ingredient
    ingredients = Column(postgresql.ARRAY(String))

    # array of strings where each element is a new paragraph of instructions
    instructions = Column(postgresql.ARRAY(String))

    recipe_collection_id = db.Column(db.Integer, db.ForeignKey('recipe_collections.id'), nullable=True)

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'ingredients': self.ingredients,
            'instructions': self.instructions
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format())


'''
RECIPE
a persistent recipe entity, extends the base SQLAlchemy Model
'''
class RecipeCollection(db.Model):
    __tablename__ = 'recipe_collections'
    id = Column(Integer, primary_key=True)
    
    # title of recipe
    title = Column(String((300)), unique=True)

    # one to many association table of collection -> recipes
    recipes = db.relationship('Recipe', backref='recipe_collection', lazy=True, cascade = "all, delete, delete-orphan")

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'recipes': self.recipes,
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format())