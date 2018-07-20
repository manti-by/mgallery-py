import pytest
from datetime import datetime

from core.conf import settings
from core.comparator import Comparator
from core.detector import Detector


class TestDlibUtils:

    @staticmethod
    def find_similar(dsc_list_1, dsc_list_2):
        for dsc_1 in dsc_list_1:
            for dsc_2 in dsc_list_2:
                if Comparator.is_descriptors_similar(dsc_1, dsc_2):
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
