from core.conf import settings
from core.comparator import Comparator
from core.detector import Detector
from test.fixtures import (
    TEST_VECTOR_1,
    TEST_VECTOR_2
)
from service import (
    DescriptorService,
    PersonService
)


class TestDlib:

    @staticmethod
    def find_similar(dsc_list_1, dsc_list_2):
        for dsc_1 in dsc_list_1:
            for dsc_2 in dsc_list_2:
                if Comparator.is_similar(dsc_1, dsc_2):
                    yield dsc_1, dsc_2

    def test_compare_two_images(self):
        test_path = '%s/%s' % (settings['gallery'], 'face-compare.jpg')
        dt_1 = Detector(test_path)
        dt_1.run()

        test_path = '%s/%s' % (settings['gallery'], 'face-detection.jpg')
        dt_2 = Detector(test_path)
        dt_2.run()

        assert len(dt_1.descriptors) == 1
        assert len(dt_2.descriptors) == 4

        similar = self.find_similar(dt_1.descriptors, dt_2.descriptors)
        assert len(list(similar)) == 1

    def test_compare_two_models(self, session):
        dsc_service = DescriptorService()
        person_service = PersonService()

        descriptor_id = dsc_service.create(vector=TEST_VECTOR_1)
        descriptor = dsc_service.get(id=descriptor_id)

        created_person_id = person_service.create(name='Test')
        dsc_service.create(vector=TEST_VECTOR_2,
                           person_id=created_person_id)

        comparator = Comparator(descriptor)
        found_person_id = comparator.find_person()

        assert created_person_id == found_person_id
