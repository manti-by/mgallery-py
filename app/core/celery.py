from celery import Celery
from imagehash import phash
from PIL import Image as PILImage

from core.conf import settings
from service.image import ImageService

app = Celery()
app.conf.broker_url = settings['celery_broker']


@app.task
def process_image(image_id):
    image = ImageService().get(id=image_id)
    if image is not None:
        image_phash = phash(
            PILImage.open(image.path)
        )
        ImageService().update(
            id=image_id, phash=image_phash
        )
