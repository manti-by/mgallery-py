import logging
import logging.config
from typing import Optional

from imagehash import phash
from PIL import Image

from mgallery.settings import LOGGING


def setup_logging(verbose_level: int = 0):
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
    logging.config.dictConfig(LOGGING)


def get_logger(name: str, verbose_level: int = 0) -> logging.Logger:
    setup_logging(verbose_level)
    return logging.getLogger(name)


def extract_image_data(path: str) -> Optional[dict]:
    result = {
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
        return result
    except Exception as e:
        get_logger(__name__).error(e)
