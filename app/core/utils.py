import os
import logging
import logging.config

from imagehash import phash
from PIL import Image

from core.conf import settings

logger = logging.getLogger()


def extract_gallery_data(path):
    return {"year": os.path.splitext(os.path.basename(path))[0]}


def extract_image_data(path):
    result = {
        "name": os.path.basename(path),
        "width": None,
        "height": None,
        "phash": None,
    }

    try:
        image = Image.open(path)
        result["width"] = image.size[0]
        result["height"] = image.size[1]
        result["phash"] = str(phash(image))
    except Exception as e:
        logger.error(e)

    return result


def setup_logging(verbose_level):
    try:
        log_level = {None: logging.ERROR, 0: logging.WARNING, 1: logging.INFO}[
            verbose_level
        ]
    except KeyError:
        log_level = logging.DEBUG

    logging.basicConfig(level=log_level)
    logging.config.dictConfig(settings["logging"])
