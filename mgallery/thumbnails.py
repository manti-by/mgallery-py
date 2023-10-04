import logging

from mgallery.database import Database
from mgallery.image import create_thumbnail

logger = logging.getLogger(__name__)


def run_thumbnails():
    for _, images in Database().duplicates().items():
        for image in images:
            if ".gif" in image["name"]:
                continue
            try:
                create_thumbnail(image["path"], image["name"])
            except Exception as e:
                logger.error(e)
                continue
