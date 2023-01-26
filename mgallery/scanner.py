import os
import glob
import logging
from typing import Awaitable

from imagehash import phash
from PIL import Image

from mgallery.settings import GALLERY_PATH
from mgallery.database import create_image, list_images

logger = logging.getLogger(__name__)


async def get_images(ext: str) -> list[str]:
    return glob.glob(f"{GALLERY_PATH}/{ext}", recursive=True)


async def process_image(path: str, name: str) -> Awaitable:
    try:
        image = Image.open(f"{GALLERY_PATH}/{path}/{name}")
        return await create_image(
            path=path,
            name=name,
            size=len(image.fp.read()),
            width=image.size[0],
            height=image.size[1],
            phash=str(phash(image)),
        )
    except Exception as e:
        logger.error(e)


async def run_scanner():
    logger.info(f"Start scanning {GALLERY_PATH}")

    existing_images = [f"{x['path']}/{x['name']}" for x in await list_images()]
    existing_images_len = len(existing_images)

    files = []
    for ext in ("**/*.jpg", "**/*.jpeg", "**/*.png", "**/*.gif"):
        files.extend(await get_images(ext))

    for current_file in files:
        name = os.path.basename(current_file)
        path = os.path.dirname(current_file).replace(GALLERY_PATH, "")[1:]

        # Skip images from the DB and all images in the gallery root
        if f"{path}/{name}" not in existing_images and path is not None:
            image_id = await process_image(path, name)
            if image_id is not None:
                existing_images.append(f"{path}/{name}")
                logger.info(f"Added image {name} to gallery {path}")

    logger.info(
        f"Finish scanning, added {len(existing_images) - existing_images_len} images"
    )
