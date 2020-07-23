import os
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects import postgresql
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

database_path = os.getenv("DATABASE URL")
# database_path = 'postgres://johkyqiaoouyph:8a57bd3636fdbaf156b74e7ca4e2a6f1621fa28be56ab2b64fb87943befa2575@ec2-35-153-12-59.compute-1.amazonaws.com:5432/dbp403t30t6sn8'


# database_name = "recipebox"
# database_path = 'postgres://williamfrancis@localhost:5432/recipebox'
# database_path = "postgres://{}/{}".format('localhost:5432', database_name)
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    

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
    __tablename__ = 'recipe'
    id = Column(Integer, primary_key=True)
    # title of recipe
    title = Column(String((300)), unique=True)

    # array of strings where each element is a new ingredient
    ingredients = Column(postgresql.ARRAY(String))

    # array of strings where each element is a new paragraph of instructions
    instructions = Column(postgresql.ARRAY(String))

    recipe_collection = db.relationship("RecipeCollection", back_populates="recipe")
    recipe_collection_id = db.Column(db.Integer, db.ForeignKey('recipe_collection.id'), nullable=True)

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'ingredients': self.ingredients,
            'instructions': self.instructions,
            'recipe_collection_id': self.recipe_collection_id
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
    __tablename__ = 'recipe_collection'
    id = Column(Integer, primary_key=True)
    
    # title of recipe
    title = Column(String(300), unique=True)

    description = Column(String, unique=True)

    # one to many association table of collection -> recipes
    recipe = db.relationship('Recipe', back_populates='recipe_collection', lazy=True, cascade = "all, delete, delete-orphan")

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'recipes': self.get_formatted_recipes(),
        }

    def get_formatted_recipes(self):
        arr = []
        for r in self.recipe:
            arr.append(r.format())
        return arr

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