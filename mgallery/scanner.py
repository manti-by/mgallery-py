import asyncio

import os
import glob
import logging
import itertools

from mgallery.phash import get_image_data
from mgallery.settings import GALLERY_PATH
from mgallery.database import create_image, get_images

logger = logging.getLogger(__name__)


async def scan_gallery(ext: str) -> list[str]:
    return glob.glob(f"{GALLERY_PATH}/{ext}", recursive=True)


async def process_file(file: str, existing_images: list[str]):
    name = os.path.basename(file)
    path = os.path.dirname(file).replace(GALLERY_PATH, "")[1:]
    if f"{path}/{name}" not in existing_images:
        try:
            width, height, image_hash = get_image_data(f"{GALLERY_PATH}/{path}/{name}")
            size = os.path.getsize(f"{GALLERY_PATH}/{path}/{name}")
            await create_image(
                path=path, name=name, phash=image_hash, width=width, height=height, size=size
            )
            logger.info(f"Processed {path}/{name}")
        except Exception as e:
            logger.error(e)


async def run_scanner():
    logger.info(f"Start scanning {GALLERY_PATH}")

    extensions = ("**/*.jpg", "**/*.jpeg", "**/*.png", "**/*.gif")
    existing_images = [f"{x['path']}/{x['name']}" for x in await get_images()]

    files = await asyncio.gather(*[scan_gallery(ext) for ext in extensions])
    await asyncio.gather(
        *[process_file(file, existing_images) for file in itertools.chain(*files)]
    )

    logger.info(f"Finish scanning, added {len(files) - len(existing_images)} images")
