import logging

from typing import Awaitable
from humanize import naturalsize

from mgallery.settings import GALLERY_PATH
from mgallery.database import get_duplicates

logger = logging.getLogger(__name__)

red = "\033[0;31m"
yellow = "\033[0;33m"
reset = "\033[0m"


async def generate_report() -> Awaitable:
    logger.info(f"Start report generation for {GALLERY_PATH}")

    grouped_images = {}
    for image in await get_duplicates():
        grouped_images.setdefault(image["phash"], []).append(image)

    current_phash = None
    for phash, images in grouped_images.items():
        if phash != current_phash:
            current_phash = phash
            logger.info(f"Duplicates {current_phash} ==============================")

        prev_width = prev_height = prev_size = None
        for image in images:
            size = naturalsize(image["size"], gnu=True)
            message = f"{GALLERY_PATH}/{image['path']}/{image['name']} {image['width']}x{image['height']} {size}"
            if (prev_width is None and prev_height is None and prev_size is None) or (
                image["width"] == prev_width
                and image["height"] == prev_height
                and image["size"] == prev_size
            ):
                logger.info(message)
            else:
                logger.info(yellow + message + reset)

            prev_width = image["width"]
            prev_height = image["height"]
            prev_size = image["size"]

    logger.info("Finish report generation")
