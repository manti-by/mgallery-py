import os
import glob

from mgallery.queue import queue
from mgallery.services import process_image
from mgallery.settings import GALLERY_PATH
from mgallery.database import GalleryService, ImageService
from mgallery.utils import get_logger

logger = get_logger(__name__)


class Scanner:
    def __init__(self, path: str):
        self.path = path
        self.gallery_service = GalleryService()
        self.image_service = ImageService()

    @property
    def file_list(self) -> list:
        files = []
        for ext in ("**/*.jpg", "**/*.jpeg", "**/*.png", "**/*.gif"):
            files.extend(glob.glob(f"{self.path}{ext}", recursive=True))
        return files

    def run(self):
        logger.info(f"Start scanning {self.path}")

        new_images = 0
        gallery_list = {x["path"]: x["id"] for x in self.gallery_service.list()}
        for current_file in self.file_list:
            current_directory = os.path.dirname(current_file)
            directory_name = current_directory.replace(GALLERY_PATH, "")
            if current_directory not in gallery_list.keys():
                gallery_id = self.gallery_service.create(
                    path=current_directory, name=directory_name
                )
                gallery_list[current_directory] = gallery_id
                logger.info(f"Added new gallery {current_directory}")
            else:
                gallery_id = gallery_list[current_directory]

            image_list = {
                x["path"]: x["id"]
                for x in self.image_service.list(gallery_id=gallery_id)
            }
            if current_file not in image_list.keys():
                file_name = os.path.basename(current_file)
                image_id = self.image_service.create(
                    gallery_id=gallery_id, path=current_file, name=file_name
                )
                new_images += 1
                image_list[current_file] = image_id
                queue.enqueue(process_image, image_id)
                logger.info(f"Added image {file_name} to gallery {directory_name}")

        logger.info(f"Finish scanning, added {new_images} images")
