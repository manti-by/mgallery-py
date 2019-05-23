import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from core.conf import settings

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_app():
    flask_app = Flask(__name__, template_folder=os.path.join(ROOT_PATH, "template"))
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = settings["database"]
    flask_app.db = SQLAlchemy(flask_app)
    return flask_app


app = create_app()
