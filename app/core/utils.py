import re
import logging

from datetime import datetime
from imagehash import phash
from PIL import Image

from core.exif import get_exif_data

logger = logging.getLogger()


def extract_gallery_data(path):
    result = {
        'year1': None,
        'year2': None,
        'date': None,
        'name': None,
    }

    try:
        path_regex = re.compile(
            '(?P<year1>\d{4})\S?(?P<year2>\d{4})?(?P<date>\d{2}-\d{2})?\s?(?P<name>.*)?'
        )

        for directory in path.split('/'):
            match = path_regex.match(directory)
            if match is not None:
                if match.group('year1'):
                    result['year1'] = match.group('year1')
                if match.group('year2'):
                    result['year2'] = match.group('year2')
                if match.group('date'):
                    result['date'] = match.group('date')
                if match.group('name'):
                    result['name'] = match.group('name')
    except Exception as e:
        logger.error(e)

    return result


def extract_image_data(path):
    result = {
        'camera': None,
        'lens': None,
        'position': None,
        'datetime': None,
        'phash': None,
    }

    try:
        image = Image.open(path)
        result['phash'] = str(phash(image))

        exif_data = get_exif_data(image)
        result['camera'] = exif_data.get('camera')
        result['lens'] = exif_data.get('lens')
        result['position'] = exif_data.get('position')
        result['datetime'] = exif_data.get('datetime')
    except Exception as e:
        logger.error(e)

    return result


