from celery import Celery

from core.conf import settings
from core.utils import (
    extract_gallery_data,
    extract_image_data
)
from service.gallery import GalleryService
from service.image import ImageService

app = Celery()
app.conf.broker_url = settings['celery_broker']


@app.task
def process_gallery(gallery_id):
    gallery = GalleryService().get(id=gallery_id)
    if gallery is not None:
        data = extract_gallery_data(gallery.path)
        return GalleryService().update(id=gallery.id,
                                       path=gallery.path, **data)


@app.task
def process_image(image_id):
    image = ImageService().get(id=image_id)
    if image is not None:
        data = extract_image_data(image.path)
        return ImageService().update(id=image.id,
                                     path=image.path, **data)
