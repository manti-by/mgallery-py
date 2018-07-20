from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy

from core.conf import settings
from model.descriptor import DescriptorModel
from model.gallery import GalleryModel
from model.image import ImageModel
from model.person import PersonModel
from service.gallery import GalleryService


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings['database']
db = SQLAlchemy(app)


class GalleryView(ModelView):
    column_list = ('path',)


class ImageView(ModelView):
    column_list = ('gallery_id', 'name')


class DescriptorView(ModelView):
    column_list = ('image_id', 'person_id')


class PersonView(ModelView):
    column_list = ('name',)


MV_MAP = [
    (DescriptorModel, DescriptorView),
    (GalleryModel, GalleryView),
    (ImageModel, ImageView),
    (PersonModel, PersonView),
]


def run_server():
    admin = Admin(app)
    for model, view in MV_MAP:
        admin.add_view(view(model, db.session))

    db.create_all()
    app.run('0.0.0.0', 8000)
