from mgallery.services import find_duplicates
from mgallery.settings import GALLERY_PATH
from mgallery.database import ImageService
from mgallery.utils import get_logger

logger = get_logger(__name__)


class Merger:
    def __init__(self):
        self.image_service = ImageService()

    def run(self, dry_run: bool = True):
        logger.info(f"Start merging images in {GALLERY_PATH}")

        counter = 0
        exclude = []
        for image in self.image_service.list():
            exclude.append(image["id"])
            duplicates = find_duplicates(image["id"], dry_run=dry_run, exclude=exclude)
            if duplicates is not None and len(duplicates):
                exclude += duplicates
            counter += 1
            if counter % 1000 == 0:
                logger.info(f"Checked {counter} images")

        logger.info(f"Finish merging, found {len(exclude) - counter} duplicates")
