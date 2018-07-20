import uuid

from celery import Celery

from core.conf import settings
from core.comparator import Comparator
from core.detector import Detector
from core.utils import (
    extract_gallery_data,
    extract_image_data
)
from service.descriptor import DescriptorService
from service.gallery import GalleryService
from service.image import ImageService
from service.person import PersonService

app = Celery()
app.conf.broker_url = settings['celery_broker']


@app.task
def process_gallery(gallery_id):
    gallery = GalleryService().get(id=gallery_id)
    if gallery is not None:
        data = extract_gallery_data(gallery.path)
        GalleryService().update(id=gallery.id, **data)
        return 'Successfully processed gallery with id %d' % gallery_id
    return 'Cant find gallery with id %d' % image_id


@app.task
def process_image(image_id):
    image = ImageService().get(id=image_id)
    if image is not None:
        data = extract_image_data(image.path)
        ImageService().update(id=image.id, **data)
        return 'Successfully processed image with id %d' % image_id
    return 'Cant find image with id %d' % image_id


@app.task
def find_faces(image_id):
    descriptors = []
    image = ImageService().get(id=image_id)
    if image is not None:
        detector = Detector(image.path)
        detector.run()
        for descriptor in detector.descriptors:
            descriptor_id = DescriptorService().create(image_id=image.id,
                                                       vector=list(descriptor))
            compare_faces.delay(descriptor_id)
            descriptors.append(descriptors)
        return 'Successfully found %d faces for image %d' % (len(descriptors), image_id)
    else:
        return 'Cant find image with id %d' % image_id


@app.task
def compare_faces(descriptor_id):
    descriptor = DescriptorService().get(id=descriptor_id)
    if descriptor is not None:
        # Trying to find similar descriptor and return its person
        def find_person(dsc):
            for personalized in DescriptorService().personalized():
                if Comparator(dsc, personalized).is_similar:
                    return personalized.person_id

        person_id = find_person(descriptor)
        if person_id is None:
            person_id = PersonService().create(
                name=uuid.uuid4().hex[:8]
            )
        DescriptorService().update(
            id=descriptor_id,
            person_id=person_id

        )
        return 'Updated descriptor with person id %d' % person_id
    else:
        return 'Cant find descriptor with id %d' % descriptor_id