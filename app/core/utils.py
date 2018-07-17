import os
import re
import logging

from datetime import datetime
from imagehash import phash
from PIL import Image

from core.exif import get_exif_data

logger = logging.getLogger()


def extract_gallery_data(path):
    result = {
        'year': None,
        'date': None,
        'name': None,
    }

    try:
        path_regex = re.compile(
            '(?P<year>\d{4})\S?(?P<ext_year>\d{4})?(?P<date>\d{2}-\d{2})?\s?(?P<name>.*)?'
        )

        for directory in path.split('/'):
            match = path_regex.match(directory)
            if match is not None:
                if match.group('year'):
                    result['year'] = match.group('year')
                if match.group('date'):
                    result['date'] = match.group('date')
                if match.group('name'):
                    result['name'] = match.group('name')
    except Exception as e:
        logger.error(e)

    if result['date'] is not None:
        result['date'] = datetime.strptime(
            '%s-%s' % (result['year'], result['date']), '%Y-%m-%d'
        ).date()

    return result


def extract_image_data(path):
    result = {
        'name': os.path.basename(path),
        'camera': None,
        'lens': None,
        'location': None,
        'datetime': None,
        'phash': None,
    }

    image = Image.open(path)
    try:
        result['phash'] = str(phash(image))
    except Exception as e:
        logger.error(e)

    try:
        exif_data = get_exif_data(image)
        result['camera'] = exif_data.get('camera')
        result['lens'] = exif_data.get('lens')
        result['location'] = exif_data.get('location')
        result['datetime'] = exif_data.get('datetime')
    except Exception as e:
        logger.error(e)

    return result
