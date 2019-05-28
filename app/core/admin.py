from flask_admin import Admin, AdminIndexView, expose
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView

from core.app import app
from core.conf import settings
from model import GalleryModel, ImageModel
from service import GalleryService, ImageService


class GalleryView(ModelView):
    column_list = ("url", "path")

    @expose("/<int:gallery_id>/")
    def item(self, gallery_id):
        gallery = GalleryService().get(id=gallery_id)
        return self.render("gallery.html", item=gallery)


class ImageView(ModelView):
    column_list = ("url", "gallery_id", "path", "similar_images")
    column_filters = ["gallery_id"]

    @expose("/<int:image_id>/")
    def item(self, image_id):
        image = ImageService().get(id=image_id)
        return self.render("image.html", item=image)


MV_MAP = [(GalleryModel, GalleryView, "gallery"), (ImageModel, ImageView, "image")]


def run_server():
    app.config["SQLALCHEMY_DATABASE_URI"] = settings["database"]

    admin = Admin(app, index_view=AdminIndexView(url="/"))
    admin.add_link(MenuLink("Flower", url="http://localhost:5555"))

    for model, view, endpoint in MV_MAP:
        admin.add_view(view(model, app.db.session, endpoint=endpoint))

    app.run("0.0.0.0", 8228)
    return app
