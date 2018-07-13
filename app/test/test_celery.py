from core.celery import (
    process_gallery,
    process_image
)
from core.conf import settings
from service.gallery import GalleryService
from service.image import ImageService


class TestCelery:

    def test_process_gallery(self):
        service = GalleryService()
        gallery_id = service.create(path='/2009-2011 Ранние/2009-11-17')
        assert gallery_id is not None

        updated_gallery_id = process_gallery(gallery_id)
        assert gallery_id == updated_gallery_id

    def test_process_image(self):
        service = ImageService()
        test_path = '%s%s' % (
            settings['gallery'], '/2017 Весна/2017-03-05 Мерс/P70305-164500.jpg'
        )
        image_id = service.create(path=test_path)
        assert image_id is not None

        updated_image_id = process_image(image_id)
        assert image_id == updated_image_id

        image = service.get(id=image_id)
        assert image.phash is not None
        assert image.camera is not None
