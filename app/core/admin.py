import logging

from flask import send_from_directory
from flask_admin import Admin, BaseView, expose
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView

from core.app import app
from core.conf import settings
from model import GalleryModel, ImageModel
from service import GalleryService, ImageService


logger = logging.getLogger()

hash(1)


class IndexView(BaseView):
    @expose("/")
    def index(self):
        logger.info("GET Index")

        gallery_list = GalleryService().list()
        return self.render("index.html", gallery_list=gallery_list)


class GalleryView(ModelView):
    column_list = ("url", "path")

    @expose("/<int:gallery_id>/")
    def item(self, gallery_id):
        logger.info(f"GET Gallery #{gallery_id}")

        gallery = GalleryService().get(id=gallery_id)
        return self.render("gallery.html", item=gallery)


class ImageView(ModelView):
    column_list = ("url", "gallery_id", "path", "similar_images")
    column_filters = ["gallery_id"]

    @expose("/<int:image_id>/")
    def item(self, image_id):
        logger.info(f"GET Image #{image_id}")

        image = ImageService().get(id=image_id)
        return self.render("image.html", item=image)


@app.route("/static/<path:filename>")
def send_static(filename):
    return send_from_directory(app.static_folder, filename)


MV_MAP = [(GalleryModel, GalleryView, "gallery"), (ImageModel, ImageView, "image")]


def run_server():
    app.config["SQLALCHEMY_DATABASE_URI"] = settings["database"]

    admin = Admin(app, index_view=IndexView(url="/"))
    admin.add_link(MenuLink("Flower", url=settings["flower_url"]))

    for model, view, endpoint in MV_MAP:
        admin.add_view(view(model, app.db.session, endpoint=endpoint))

    logger.info("Run app")
    app.run(settings["host"], settings["port"])

    return app
