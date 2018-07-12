from unittest import TestCase

from core.celery import (
    process_gallery,
    process_image
)
from service.gallery import GalleryService
from service.image import ImageService


class CeleryTestCase(TestCase):

    def test_process_gallery(self):
        service = GalleryService()
        gallery_id = service.create(path='/2009-2011 Ранние/2009-11-17')
        self.assertIsNotNone(gallery_id)

        updated_gallery_id = process_gallery(gallery_id)
        self.assertEqual(gallery_id, updated_gallery_id)

    def test_process_image(self):
        service = ImageService()
        image_id = service.create(path='/2017 Весна/2017-03-05 Мерс/P70305-164500.jpg')
        self.assertIsNotNone(image_id)

        updated_image_id = process_image(image_id)
        self.assertEqual(image_id, updated_image_id)
