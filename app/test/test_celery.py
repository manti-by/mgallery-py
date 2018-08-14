import uuid

from core.celery import (
    process_gallery,
    process_image,
    find_duplicates
)
from core.conf import settings
from service.gallery import GalleryService
from service.image import ImageService


class TestCelery:

    def test_process_gallery(self, session):
        service = GalleryService()
        gallery_id = service.create(path='/2009-2011 Ранние/2009-11-17')
        assert gallery_id is not None

        result = process_gallery(gallery_id)
        assert result == 'Successfully processed gallery with id %d' % gallery_id

    def test_process_image(self, session):
        service = ImageService()
        test_path = '%s%s' % (
            settings['gallery'], '/2017 Весна/2017-03-05 Мерс/P70305-164500.jpg'
        )
        image_id = service.create(path=test_path)
        assert image_id is not None

        result = process_image(image_id)
        assert result == 'Successfully processed image with id %d' % image_id

        image = service.get(id=image_id)
        assert image.phash is not None
        assert image.camera is not None

    def test_similar_images(self, session):
        service = ImageService()
        test_path = '/2017 Весна/2017-03-05 Мерс/P70305-164500.jpg'
        test_phash = uuid.uuid4().hex[:8]

        image_1_id = service.create(path=test_path, phash=test_phash)
        assert image_1_id is not None

        image_2_id = service.create(path=test_path, phash=test_phash)
        assert image_2_id is not None

        result = find_duplicates(image_1_id)
        assert result == 'Successfully found 1 duplicates for image %d' % image_1_id

        image_1 = service.get(id=image_1_id)
        image_2 = service.get(id=image_2_id)
        assert image_1.similar.all() == [image_2]
