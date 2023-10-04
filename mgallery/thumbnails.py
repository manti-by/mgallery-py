import logging

from mgallery.database import Database
from mgallery.image import create_thumbnail

logger = logging.getLogger(__name__)


def run_thumbnails():
    counter = 0
    for _, images in Database().duplicates().items():
        for image in images:
            if ".gif" in image["name"]:
                continue
            try:
                create_thumbnail(image["path"], image["name"])
            except Exception as e:
                logger.error(e)
                continue

            if (counter := counter + 1) % 500 == 0:
                logger.info(f"Created {counter} thumbnails")
