import os

from flask_sqlalchemy import SQLAlchemy

from .web import app


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', None)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

assert app.config['SQLALCHEMY_DATABASE_URI'], 'Specify SQLALCHEMY_DATABASE_URI as environment variable.'

db = SQLAlchemy(app)
