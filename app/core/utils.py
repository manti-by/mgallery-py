import os
import logging
import logging.config

from imagehash import phash
from PIL import Image

from core.conf import settings

logger = logging.getLogger()


def extract_gallery_data(path):
    return {"name": os.path.splitext(os.path.basename(path))[0]}


def extract_image_data(path):
    result = {
        "name": os.path.basename(path),
        "size": 0,
        "width": None,
        "height": None,
        "phash": None,
    }

    try:
        image = Image.open(path)
        result["size"] = len(image.fp.read())
        result["width"] = image.size[0]
        result["height"] = image.size[1]
        result["phash"] = str(phash(image))
    except Exception as e:
        logger.error(e)

    return result


def setup_logging(verbose_level):
    try:
        log_level = {
            0: logging.CRITICAL,
            1: logging.ERROR,
            2: logging.WARNING,
            3: logging.INFO,
            4: logging.DEBUG,
        }[int(verbose_level or 0)]
    except KeyError:
        log_level = logging.DEBUG

    logging.basicConfig(level=log_level)
    logging.config.dictConfig(settings["logging"])
