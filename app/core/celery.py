from celery import Celery

from core.conf import settings
from core.detector import Detector
from core.utils import (
    extract_gallery_data,
    extract_image_data
)
from service.descriptor import DescriptorService
from service.gallery import GalleryService
from service.image import ImageService

app = Celery()
app.conf.broker_url = settings['celery_broker']


@app.task
def process_gallery(gallery_id):
    gallery = GalleryService().get(id=gallery_id)
    if gallery is not None:
        data = extract_gallery_data(gallery.path)
        return GalleryService().update(id=gallery.id, **data)
    return None


@app.task
def process_image(image_id):
    image = ImageService().get(id=image_id)
    if image is not None:
        data = extract_image_data(image.path)
        return ImageService().update(id=image.id, **data)
    return None


@app.task
def find_faces(image_id):
    descriptors = []
    image = ImageService().get(id=image_id)
    if image is not None:
        detector = Detector(image.path)
        detector.run()
        for descriptor in detector.descriptors:
            DescriptorService().create(image_id=image.id,
                                       vector=list(descriptor))
            descriptors.append(descriptors)
    return descriptors
