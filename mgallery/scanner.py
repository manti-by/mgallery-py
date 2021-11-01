import os
import glob
import logging

import asyncio
from concurrent import futures

from typing import Awaitable

from imagehash import phash
from PIL import Image

from mgallery.settings import GALLERY_PATH
from mgallery.database import create_image, list_images

logger = logging.getLogger(__name__)


async def process_image(path: str, name: str) -> Awaitable[int]:
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


async def process_files(files: list, existing_images: list) -> Awaitable:
    for current_file in files:
        name = os.path.basename(current_file)
        path = os.path.dirname(current_file).replace(GALLERY_PATH, "")[1:]

        # Skip images from the DB
        if f"{path}/{name}" not in existing_images:
            await process_image(path, name)
            logger.info(f"Added image {name} to gallery {path or 'root'}")


def create_async_process(files: list, existing_images: list):
    logger.info(f"Run new core thread with PID {os.getpid()}")
    asyncio.run(process_files(files, existing_images))


def run_scanner(num_cores=os.cpu_count()):
    logger.info(f"Start scanning {GALLERY_PATH}")

    existing_images = [f"{x['path']}/{x['name']}" for x in list_images()]
    files = []
    for ext in ("**/*.jpg", "**/*.jpeg", "**/*.png", "**/*.gif"):
        files.extend(glob.glob(f"{GALLERY_PATH}/{ext}", recursive=True))

    chunk_size = len(files) // num_cores + 1
    file_chunks = [files[i: i + chunk_size] for i in range(len(files))[::chunk_size]]

    processes = []
    with futures.ProcessPoolExecutor(max_workers=num_cores) as executor:
        for i in range(num_cores):
            processes.append(
                executor.submit(create_async_process, file_chunks[i], existing_images)
            )

    for f in futures.as_completed(processes):
        logger.info(f"Thread {f} is completed")
