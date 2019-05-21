from celery import Celery

from core.conf import settings
from core.utils import extract_gallery_data, extract_image_data
from service import GalleryService, ImageService

app = Celery()
app.conf.broker_url = settings["celery_broker"]
app.conf.ONCE = {
    "backend": "celery_once.backends.Redis",
    "settings": {"url": settings["celery_broker"], "default_timeout": 60},
}


@app.task
def process_gallery(gallery_id):
    service = GalleryService()
    gallery = service.get(id=gallery_id)
    if gallery is not None:
        data = extract_gallery_data(gallery.path)
        service.update(id=gallery.id, **data)
        return "Successfully processed gallery with id %d" % gallery_id
    return "Cant find gallery with id %d" % gallery_id


@app.task
def process_image(image_id):
    service = ImageService()
    image = service.get(id=image_id)
    if image is not None:
        data = extract_image_data(image.path)
        service.update(id=image.id, **data)
        return "Successfully processed image with id %d" % image_id
    return "Cant find image with id %d" % image_id


@app.task
def find_duplicates(image_id):
    duplicates = 0
    service = ImageService()
    image = service.get(id=image_id)
    if image is not None:
        for duplicate in service.list():
            if image.phash == duplicate.phash and image.id != duplicate.id:
                image.similar.append(duplicate)
                duplicates += 1
        service.commit([image])
        return "Successfully found %d duplicates for image %d" % (duplicates, image_id)
    else:
        return "Cant find image with id %d" % image_id
