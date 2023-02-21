import cv2
import os
import logging

from mgallery.phash import get_image_phash
from mgallery.settings import GALLERY_PATH
from mgallery.database import Database

logger = logging.getLogger(__name__)


def process_image(database: Database, path: str, name: str):
    size = os.path.getsize(f"{GALLERY_PATH}/{path}/{name}")
    try:
        width = height = phash = None
        image = cv2.imread(f"{GALLERY_PATH}/{path}/{name}")
        if image is not None:
            phash = get_image_phash(image)
            width, height = image.shape[0], image.shape[1]
        database.create(
            path=path, name=name, width=width, height=height, phash=phash, size=size
        )
    except Exception as e:
        logger.error(e)


def process_image_list(files: list, existing_images: list):
    database = Database()
    for current_file in files:
        name = os.path.basename(current_file)
        path = os.path.dirname(current_file).replace(GALLERY_PATH, "")[1:]
        if f"{path}/{name}" not in existing_images:
            process_image(database, path, name)
            logger.debug(f"Added image {name} to gallery {path or 'root'}")
