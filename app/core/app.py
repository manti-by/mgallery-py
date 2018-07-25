from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from core.conf import settings


def create_app():
    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings['database']
    flask_app.db = SQLAlchemy(flask_app)
    return flask_app


app = create_app()
