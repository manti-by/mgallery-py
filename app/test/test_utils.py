import os
from datetime import datetime
from unittest import TestCase

from core.conf import GALLERY_PATH
from core.utils import (
    extract_gallery_data,
    extract_image_data
)


class UtilsTestCase(TestCase):

    def test_extract_gallery_data(self):
        data = extract_gallery_data('/2009-2011 Ранние/2009-11-17')
        self.assertEqual(data, {
            'year1': '2009',
            'year2': '2011',
            'date': '11-17',
            'name': 'Ранние',
        })

        data = extract_gallery_data('/2017 Весна/2017-03-05 Мерс')
        self.assertEqual(data, {
            'year1': '2017',
            'year2': None,
            'date': '03-05',
            'name': 'Мерс',
        })

        data = extract_gallery_data('/2009-2011 Ранние/2009-05-01 Test')
        self.assertEqual(data, {
            'year1': '2009',
            'year2': '2011',
            'date': '05-01',
            'name': 'Test',
        })

    def test_extract_image_data(self):
        image_path = os.path.join(
            GALLERY_PATH, '2009-2011 Ранние', '2009-05-01 Test', 'DSC00144.jpeg'
        )
        data = extract_image_data(image_path)
        self.assertEqual(data, {
            'camera': None,
            'lens': None,
            'position': None,
            'datetime': None,
            'phash': '9f916066a759496d',
        })

        image_path = os.path.join(
            GALLERY_PATH, '2017 Весна', '2017-03-05 Мерс', 'P70305-164500.jpg'
        )
        data = extract_image_data(image_path)
        self.assertEqual(data, {
            'camera': 'Meizu PRO 6',
            'lens': None,
            'position': '53.96010969444445, 27.538057305555558',
            'datetime': datetime.strptime('2017-03-05 16:45:02', '%Y-%m-%d %H:%M:%S'),
            'phash': 'edc1d22d05d03e8f',
        })

        image_path = os.path.join(
            GALLERY_PATH, '2018 Весна', '2018-05-05 Барселона', '2018-05-08_12-14-46-56.jpg'
        )
        data = extract_image_data(image_path)
        self.assertEqual(data, {
            'camera': 'SONY SLT-A77V',
            'lens': 'DT 16-50mm F2.8 SSM',
            'position': '41.591363333333334, 1.8356766666666666',
            'datetime': datetime.strptime('2018-05-08 12:14:46', '%Y-%m-%d %H:%M:%S'),
            'phash': 'cc87cdc4d678b922',
        })
