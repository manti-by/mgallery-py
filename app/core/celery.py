import os
import logging

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

logger = logging.getLogger()


@app.task
def process_gallery(gallery_id):
    service = GalleryService()
    gallery = service.get(id=gallery_id)
    if gallery is not None:
        data = extract_gallery_data(gallery.path)
        service.update(id=gallery.id, **data)
        return f"Successfully processed gallery with id {gallery_id}"
    return f"Cant find gallery with id {gallery_id}"


@app.task
def process_image(image_id):
    service = ImageService()
    image = service.get(id=image_id)
    if image is not None:
        data = extract_image_data(image.path)
        service.update(id=image.id, **data)
        return f"Successfully processed image with id {image_id}"
    return f"Cant find image with id {image_id}"


@app.task
def find_duplicates(image_id):
    duplicates = 0
    removed = 0
    service = ImageService()
    image = service.get(id=image_id)
    if image is not None:
        for duplicate in service.list():
            if image.phash == duplicate.phash and image.id != duplicate.id:
                if (
                    image.size == duplicate.size
                    and image.width == duplicate.width
                    and image.height == duplicate.height
                ):
                    os.remove(duplicate.path)
                    service.delete(duplicate)
                    removed += 1

                    logger.info(f"Removed duplicate {duplicate.path}")
                else:
                    image.similar.append(duplicate)
                duplicates += 1
        service.add(image)
        return (
            f"Successfully found {duplicates} duplicates for "
            "image {image_id}, automatically removed {removed}"
        )
    else:
        return f"Cant find image with id {image_id}"
