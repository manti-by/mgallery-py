import logging
import logging.config

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
    """Used to override RQ logging config app services"""
    setup_logging(verbose_level)
    return logging.getLogger(name)
