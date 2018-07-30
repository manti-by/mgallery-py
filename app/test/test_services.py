from service.gallery import GalleryService
from service.image import ImageService


class TestServices:

    def test_gallery_service(self, session):
        test_path = '/2009-2011 Ранние/2009-11-17'
        service = GalleryService()
        gallery_id = service.create(path=test_path)
        assert gallery_id is not None

        gallery = service.get(id=gallery_id)
        assert gallery is not None
        assert gallery.id == gallery_id
        assert gallery.path == test_path
        assert gallery.name is None

        test_name = 'Test'
        updated_gallery_id = service.update(id=gallery_id, name=test_name)
        assert gallery_id == updated_gallery_id

        gallery = service.get(id=gallery_id)

        assert gallery is not None

        assert gallery.id == gallery_id
        assert gallery.path == test_path
        assert gallery.name == test_name

    def test_image_service(self, session):
        test_path = '/2017 Весна/2017-03-05 Мерс/P70305-164500.jpg'
        service = ImageService()
        image_id = service.create(path=test_path)
        assert image_id is not None

        image = service.get(id=image_id)
        assert image is not None
        assert image.id == image_id
        assert image.path == test_path
        assert image.name is None

        test_name = 'Test'
        test_width = 1920
        test_height = 1280
        updated_image_id = service.update(id=image_id, name=test_name,
                                          width=test_width, height=test_height)
        assert image_id == updated_image_id

        image = service.get(id=image_id)
        assert image is not None

        assert image.id == image_id
        assert image.path == test_path
        assert image.name == test_name

        assert image.width == test_width
        assert image.height == test_height
