from flask_admin import Admin, AdminIndexView
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView

from core.app import app
from core.conf import settings
from model import (
    DescriptorModel,
    GalleryModel,
    ImageModel,
    PersonModel
)


class GalleryView(ModelView):
    column_list = ('id', 'path',)


class ImageView(ModelView):
    column_list = ('id', 'gallery_id', 'name')


class DescriptorView(ModelView):
    column_list = ('id', 'image_id', 'person_id')


class PersonView(ModelView):
    column_list = ('id', 'name',)


MV_MAP = [
    (DescriptorModel, DescriptorView),
    (GalleryModel, GalleryView),
    (ImageModel, ImageView),
    (PersonModel, PersonView),
]


def run_server():
    app.config['SQLALCHEMY_DATABASE_URI'] = settings['database']

    admin = Admin(app, index_view=AdminIndexView(url='/'))
    admin.add_link(
        MenuLink('Flower', url='http://localhost:5555')
    )

    for model, view in MV_MAP:
        admin.add_view(view(model, app.db.session))

    app.run('0.0.0.0', 8000)
    return app
