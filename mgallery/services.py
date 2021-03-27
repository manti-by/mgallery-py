import os
from typing import Optional

from mgallery.utils import extract_image_data
from mgallery.database import ImageService, GalleryService
from mgallery.utils import get_logger

logger = get_logger(__name__)


def process_image(image_id: int) -> Optional[dict]:
    service = ImageService()
    image = service.get(image_id=image_id)
    if image is None:
        logger.error(f"Cant find image with id {image_id}")
        return

    data = extract_image_data(image["path"])
    service.update(image_id=image["id"], **data)
    logger.info(f"Successfully processed image with id {image_id}")
    return data


def find_duplicates(
    image_id: int, dry_run: bool = True, exclude: list = None
) -> Optional[list]:
    duplicates = []
    image_service = ImageService()
    image = image_service.get(image_id=image_id)

    if image is None:
        logger.error(f"Cant find image with id {image_id}")
        return

    if not all((image["phash"], image["width"], image["height"])):
        logger.debug(f"Skip {image['path']} with empty pHash and size data")
        return

    gallery_service = GalleryService()
    gallery = gallery_service.get(gallery_id=image["gallery_id"])
    for duplicate in image_service.list(exclude=exclude):
        if not all((duplicate["phash"], duplicate["width"], duplicate["height"])):
            logger.debug(f"Skip {duplicate['path']} with empty pHash and size data")
            continue

        if image["phash"] == duplicate["phash"] and image["id"] != duplicate["id"]:
            if (
                image["size"] == duplicate["size"]
                and image["width"] == duplicate["width"]
                and image["height"] == duplicate["height"]
            ):
                duplicates.append(duplicate)
                if not dry_run:
                    os.remove(duplicate["path"])
                    image_service.delete(duplicate["id"])

    if len(duplicates) > 0:
        logger.info(
            f"Found {len(duplicates)} duplicates for image {gallery['name']}/{image['name']}:"
        )
        for duplicate in duplicates:
            gallery = gallery_service.get(gallery_id=duplicate["gallery_id"])
            logger.info(f"    {gallery['name']}/{duplicate['name']}")

    return [x["id"] for x in duplicates]
