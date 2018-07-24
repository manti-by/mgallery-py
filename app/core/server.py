from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from core.app import app
from model import (
    DescriptorModel,
    GalleryModel,
    ImageModel,
    PersonModel
)


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
    app.config['SQLALCHEMY_DATABASE_URI'] = settings['database']

    admin = Admin(app)
    for model, view in MV_MAP:
        admin.add_view(view(model, app.db.session))

    app.run('0.0.0.0', 8000)